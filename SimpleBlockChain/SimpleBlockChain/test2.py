#coding=utf-8

import uuid
import os
from works.actions import work
import hashlib
import json
import Queue
from threading import Thread
import numpy as np
import cv2
import base64
import jwt
import tornado.gen
from handlers.base_handler import BaseWebSocket
from config import MEDIA_ROOT
import time

message_queue = Queue.PriorityQueue()


def work_loop():
    while True:
        task = message_queue.get()

        iuuid = task.uuid
        offset_top = task.offset_top
        image_data = task.image_data
        channel = task.channel
        zoom = task.zoom
        rType = task.rType
        responseType = task.responseType

        print(">>> len: %d | current offset: %d" % (message_queue.qsize(), offset_top))

        filename = str(uuid.uuid1()) + '.jpg'
        filepath = os.path.join(MEDIA_ROOT, filename)

        with open(filepath, 'wb') as f:
            f.write(image_data.decode("base64"))

        if zoom != 1.0:
            im = cv2.imread(filepath)

            if im is None:
                continue

            osize = im.shape[1], im.shape[0]
            size = int(im.shape[1] * zoom), int(im.shape[0] * zoom)
            im = cv2.resize(im, size)
            cv2.imwrite(filepath, im)

        try:
            reply = work(filepath, use_crop=False, result=rType,responseType=responseType)
        except Exception as e:
            print("!!!!!! %s -> %s caused error" % (iuuid, filename))
            print(e)
            cmd = u"cp %s %s" % (filepath, os.path.join(MEDIA_ROOT, 'rb_' + filename))
            os.system(cmd.encode('utf-8'))
            continue


        if responseType == 'url':
            # rtn_url = 'http://101.236.17.104:3389/upload/' + 'rb_' + filename
            rtn_url = 'http://127.0.0.1:8000/upload/' + 'rb_' + filename
            reply = {'url': rtn_url, 'uuid': iuuid}

        reply['uuid'] = iuuid
        channel.write_message({'text': json.dumps(reply)})
        print '%s end time:' % channel, time.time()


class BrowserWebSocket(BaseWebSocket):

    '''浏览器websocket服务器'''


    def open(self):
        '''新的WebSocket连接打开时被调用'''
        # message = {}
        # remote_ip = self.request.remote_ip
        # message['query_string']=self.get_argument('query_string')
        # message['remote_ip']=remote_ip
        # auth, error = verify_auth_token(message)
        auth = True
        error = 'error'

        if not auth:
            reply = json.dumps({'error': error})
            self.write_message({'text': reply, 'close': True})
        else:
            reply = "{}"
            self.write_message({'text': reply})
            print(">>> %s connected" % self.request.remote_ip)


    def on_message(self, message):
        '''连接收到新消息时被调用'''
        print '%s start time:'%self,time.time()
        task = Task.create(message,self)

        if task:
            message_queue.put(task)

    @tornado.gen.coroutine
    def on_messages(self, message):
        '''连接收到新消息时被调用'''
        task = Task.create(message,self)

        if task:
            message_queue.put(task)


    def on_close(self):
        '''客户端关闭时被调用'''
        print("<<< %s disconnected" % str(self.request.remote_ip))
        # with message_queue.mutex:
        #     message_queue.queue.clear()
        while not message_queue.empty():
            try:
                message_queue.get(False)
            except Queue.Empty:
                continue

            message_queue.task_done()


    def check_origin(self, origin):
        '''允许WebSocket的跨域请求'''

        return True

class Task(object):
    def __init__(self, uuid, offset_top, image_data, channel, zoom, rType, responseType, *args):
        self.uuid = uuid
        self.offset_top = int(float(offset_top))
        self.image_data = image_data
        self.channel = channel
        self.zoom = zoom
        self.rType = rType
        self.responseType = responseType

    @classmethod
    def create(clz, message,sel):
        # data = message.get('text')
        data = message

        try:
            params = json.loads(data[:150])

            image_data = data[150:]
            image_data = image_data.replace(" ", "+")

            params['image_data'] = image_data
            params['channel'] = sel

            # add Type
            if params.get('responseType') is None:
                params['responseType'] = 'url'

            # request type
            if params.get('rType') is None:
                params['rType'] = 'rl'

            task = Task(**params)


        except ValueError as e:
            task = None
            print(">>>message data error!")
            print(e)

        return task

    def __cmp__(self, other):
        return cmp(self.offset_top, other.offset_top)



def verify_auth_token(message):
    '''token 验证'''

    token = message.get('query_string')
    secret_key = 'aoiakai'

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        if payload.get('ip') != message.get('remote_ip'):
            return False, 'ip mismatch'
    except jwt.ExpiredSignatureError as e:
        print(e)
        return False, 'token expired'
    except Exception as e:
        print(e)
        return False, 'enter correct token'

    return True, ''


work_thread = Thread(target=work_loop)
work_thread.daemon = True
work_thread.start()
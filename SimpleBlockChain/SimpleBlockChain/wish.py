#!/usr/bin/env python
# encoding:utf-8

import requests
import json
from conf import STORE_DICT_LIST
import time




store_list = STORE_DICT_LIST
store_name = 'sandbox_001'
myaccess_token =  store_list[store_name]['access_token']




class Authorize():
    def __init__(self):
        pass
    def get_authorize(self, client_id):
        """
        :return:返回授权的url + code , code 给get_token 使用
        授权成功之后得到一个url： redirect_uri&code=ede9c269-10d3-44ca-88d6-53030311de04
        其中,redirect_uri为在wish后台设置好的。
        """
        authorize_url = "https://merchant.wish.com/oauth/authorize?client_id=%s" % client_id
        req = requests.get(authorize_url)
        return req.text
        print req.text


    # def get_product_online(self,name,access_token,refresh_token,client_id,idwish_account,merchant_user_id,client_secret):
    #     access_token_url = "https://merchant.wish.com/api/v2/oauth/access_token"
    #     postdict={
    #         "name":name,
    #         "access_token":myaccess_token,
    #         "refresh_token":refresh_token,
    #         "client_id":client_id,
    #         "idwish_account":idwish_account,
    #         "merchant_user_id":merchant_user_id,
    #         "client_secrect":client_secret
    #     }
    #     return 1

    def get_token(self, code, client_id, client_secret, redirect_uri=None):
        """
        : return : 返回 json
        u'{"message":"",
           "code":0,
           "data":{"expiry_time":1465132728,
           "token_type ":"access_token",
           "access_token":"84aeb5997b6d4c83a99b1a22ee6423b6",
           "expires_in":2591976,"merchant_user_id":"57298cbd15abf85958e9f87a",
           "refresh_token":"b0bd8eec162d4aaf87d0e6aaf43729f7"}}'
        """
        if not redirect_uri:
            redirect_uri = "https://localhost/"
        access_token_url = "https://merchant.wish.com/api/v2/oauth/access_token"

        postdict = {"client_id":client_id,
                    "client_secret": client_secret,
                    "code":code,
                    "grant_type":"authorization_code",
                    "redirect_uri": redirect_uri}
        print postdict
        req = requests.post(access_token_url, data = postdict)
        token_json = eval(req.text)
        print token_json
        return token_json

    def refresh_token(self,client_id, client_secret, refresh_token):
        """
        更新token
        """
        refresh_url = "https://merchant.wish.com/api/v2/oauth/refresh_token"
        #refresh_url = "https://sandbox.merchant.wish.com/api/v2/oauth/refresh_token"

        postdict = { "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                   }
        req = requests.post(refresh_url, data = postdict)
        new_token_json = eval(req.text)
        return new_token_json


class Wish(object):
    # https://china-merchant.wish.com/api/v2/
    """
    对wish的接口api做一个整合，主要设计到产品上架相关接口
    以及之后需要处理的订单下载接口
    """
    def __init__(self, *access_token):
        if access_token:
            self.access_token = access_token
        else:
            self.access_token = myaccess_token
        self.base_url  =  "https://china-merchant.wish.com/api/v2/"
#         self.base_url = "https://sandbox.merchant.wish.com/api/v2/"




    def __make_call(self, func, **params):
        """
        func: /product/add ，调用的函数  post提交
        **params: 参数
        """
        urls = self.base_url + func
        urls = urls.split("://")
        urls = urls[0] + "://" + urls[1].replace("//","/")
        print "urls: ", urls
        data_params = {}
        data_params.update({"access_token":self.access_token})
        if params:
            data_params.update(**params)
        req = requests.post(urls, data = data_params, verify=False)
        return req.text

    def func_call(self, func, **params):
        """
        将返回的结果变为字典，如果可以转变成字典的话
        """
        result = self.__make_call(func, **params)
        try:
            result = json.loads(result)
        except Exception, e:
#             print "result: ", result
            print "json loads result Error, %s" % e
            result = {}
        return result

    def query_params(self,func, params_list, **params):
        """ 检查参数 """
        message = ""
        for param in params_list:
            if not params.get(param):
                message = "%s , 参数不全, 没有找到参数: %s " % (str(func), param)
                break
        return message

    #-----------------------------------------------------------------
    # ---------------------- 订单相关  --------------------------------
    def fetch_order_id(self, **params):
        """
        func: 根据order_id来获取 订单
        :param params:
        {
            "id": 123456789009876543210164
        }
        """
        func ="/order"
        result = {}
        if not params.get("id"):
            print "input a id in params, please!"
            return result
        result = self.func_call(func, **params)
        return result



    def fetch_all_order(self, **params):
        """
        func: 获取所有订单
         :param params:
            {
              "start": 0,    
              "limit": 100,  
              "since": "2016-4-1"
            }
        """
        func = "/order/multi-get"
        result = {}
        start, limit = 0, 15
        since = "2016-4-1"
        if params.get("start", ""): start = params.get("start")
        if params.get("limit", ""): limit = params.get("limit")
        if params.get("since", ""): since = params.get("since") 
        params = {"start": start, "count": limit, "since": since}
        tmp_result = self.func_call(func, **params)
        result = tmp_result
        while len(tmp_result.get("data", [])) >= limit:
            start += limit
            print "start: ", start
            tmp_result = self.func_call(func, **params)
            result.get("data").extend(tmp_result.get("data",[]))
            print "tmp_result: ", tmp_result
            time.sleep(0.5)
        return result

    def get_fulfill_order(self,**params):
        """
        func:获取需要处理的订单
        :param params:
        {

        }
        """
        func = 'order/get-fulfill'
        result ={}
        start ,limit = 0,50
        since = "2016-4-1"
        if params.get("start", ""): start = params.get("start")
        if params.get("limit", ""): limit = params.get("limit")
        if params.get("since", ""): since = params.get("since") 
        params = {"start": start, "count": limit, "since": since}
        tmp_result = self.func_call(func, **params)
        result = tmp_result
        print len(result)
        while len(tmp_result.get("data", [])) >limit:
            params ['start']=start
            tmp_result = self.func_call(func, **params)
            result.get("data").extend(tmp_result.get("data",[]))
            time.sleep(0.5)
            start +=limit

        return result
    def cancel_order(self, **params):
        """
        func: 退货,取消订单
        :param params 
        {
            "id": "",           #order_id
            "reason_code": 18,  #取消原因的代码
            "reason_note": "",  #原因解释，当选择-1的时候
        }

        :return 
        {
        'code': 0,
        'data': {'success': True},
        'message': ''
        }    

        ------------------------------
            -1    其他
            18    误下单了
            20    配送时间过长
            22    商品不合适
            23    收到错误的商品
            24    商品为假冒伪劣品
            25    商品已损坏
            26    商品与描述不符
            27    商品与清单不符
            30    产品被配送至错误的地址
            31    用户提供了错误的地址
            32    商品退还至发货人
           33    Incomplete Order
            34    店铺无法履行订单
            35    此件显示已妥投，但客户未收到。
           1001    Received the wrong color
           1002    Item is of poor quality
            1004    Product listing is missing information
            1005    Item did not meet expectations
            1006    Package was empty
        """
        result = {}
        func = "/order/refund"
        if not params.get("id") or not params.get("reason_code"):
            print "参数不正确, 确保有参数id, 和reason_code"
            return result
        result = self.func_call(func, **params)
        return result

    def modify_tracking(self, **params):
        """
        func: 修改已装运订单的跟踪 
        :param params
        {
            "id":"",    #order_id
            "tracking_provider": "USPS",
            "tracking_number": "12345678"   #快递号
            "ship_note": "给用户的注意", 可以不填写这个参数
        }
        """
        result = {}
        func = "/order/modify-tracking"
        if not params.get("id") or not params.get("tracking_provider") or not params.get("tracking_number"):
            print "参数不正确,确保有{'id':''，'tracking_provider':'', 'tracking_number':''} ..."
            return result
        result = self.func_call(func, **params)
        return result


    def fulfile_one_order(self, **params): 
        """ 
        func: 标志为已发货
        :param params
         {
            "id" : "57242e8c0000000000000000",
            "tracking_provider" : "USPS", 
            "tracking_number" : "12345678" ,
          }

        return :
        {
          u'message': u'Your order is being processed right now!', 
          u'code': 0,
          u'data': {u'success': True}
        }
        """
        func = "/order/fulfill-one"
        result = {}
        if not params.get("id") or not params.get("tracking_provider") or not params.get("tracking_number"):
            print "参数不正确，确保参数含有 {'id':'', 'tracing_provider':'', 'tracking_number':''} "
            return result
        result  = self.func_call(func, **params)
        return result




     #----------------------------------------------------------------
     #------------------------- wishAPI产品相关接口 ------------------------------
    """
    /product
    /product/multi-get
    /product/update
    /product/enable
    /product/disable
    /product/add
    /product/create-download-job
    /product/get-download-job-status
    /product/cancel-download-job
    """

    def retrieve_product(self, **params):
        """
            func: 检索在wish平台上存在的产品的详细信息。
            :param params
            {
                "id": "",
                "parent_sku": "",
            }
            @return 返回一个产品实体 字典类型
        """
        func = "/product"
        result = {}
        params_list = ["id", "parent_sku"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result


    def product_add(self, **params):
        """
        func: 添加产品
        :param params
         {
             "name": "产品名称",                   #必须
             "description": "产品描述",           #必须
             "tags": "关键字",                     #必须
             "sku": "sku",                     #必须
             "color": "颜色",  #可选，部分没有
             "size": "尺寸",   #可选
             "inventory": "库存",                  #必须
             "price": "",                       #必须
             "shipping": "配送",                #必须
             "msrp":"可选的制造商建议零售价",
             "shipping_time": "时间",
             "main_image": "",                  #必须
             "parent_sku": "",
             "brand": "产品厂商或牌子",
             "landing_page_url": "登入页码链接",
             "upc": "商品条码",
             "extra_images": "其他的图片",  #用了 '|' 分割
         }
        """
        func = "/product/add"
        result = {}
        params_list = ["name", "description", "tags", "sku", "inventory", "price", "main_image", "shipping"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        print result
        return result

    def update_product(self, **params):
        """ 
            func : 更新产品信息, 更新name，description, tags
            :param params 
              { 
                  "id": "",               #必须 
                  "parent_sku": "",       #必须
                  "name": "",
                  "description": "",
                  "tags": "",
                  "brand": "",
                  "landing_page_url": "",
                  "upc": "",
                  "main_image": "",
                  "extra_images": "",
              }
        """
        func = "/product/update"
        result = {}
        params_list = ["id", "parent_sku"]
        message  = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result


    def enable_product(self, **params):
        """
        func:  使一个产品可以出售
          :param params
          {
              "id": "",
              "parent_sku": ""
          }
        """
        func = "/product/enable"
        result =  {}
        params_list = ["id", "parent_sku"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result  = self.func_call(func, **params)
        return result


    def disable_product(self, **params):
        """
         func:  停止一个产品可出售
          :param params
           {
               "id": "",
               "parent_sku": "",
           }
        """
        func = "/product/disable"
        params_list = ["id", "parent_sku"]
        result = {}
        message  = self.query_params(func, params_list, **params)
        if message: 
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result
    def list_all_products(self, **params):
        """ 
            func: 列出所有产品
            :param params
            {
                "start": "0",
                "limit": "30",
                "since": "2016-4-1",
            }
        """
        result = {}
        func = "/product/multi-get"
        start, limit = 0, 15
        since = "2016-4-1"
        if params.get("start", ""): start = params.get("start")
        if params.get("limit", ""): limit = params.get("limit")
        if params.get("since", ""): since = params.get("since") 
        params = {"start": start, "count": limit, "since": since}
        tmp_result = self.func_call(func, **params)
        result = tmp_result
        while len(tmp_result.get("data", [])) >= limit:
            start += limit
            print "start: ", start
            tmp_result = self.func_call(func, **params)
            result.get("data").extend(tmp_result.get("data",[]))
            print "tmp_result: ", tmp_result
            time.sleep(0.5)
        return result


    def remove_extra_images(self, **params):
        """
            func: 移除extra图片
            :param params
            {
                "id":"",         #产品id
                "parent_sku":"",
            }
        """
        result = {}
        func = "/product/remove-extra-images"
        params_list = ["id", "parent_sku"]
        message = self.query_params(func, params_list, **params)
        if message: 
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result


    #----------------------------------------------------------------------------
    #------------------------------  创建新产品属性相关 --------------------------

    def variant_add(self, **params):
        """ 
            func: 属性添加。比如已经有一个产品有红色属性，但是想添加一个size=12的属性,则用此api
            :param params
         {
             "parent_sku": "产品名称",                   #必须
             "sku": "sku",                     #必须
             "color": "颜色",                       #    颜色与尺寸，不能同时为空
             "size": "尺寸",                        #
             "inventory": "库存",                  #必须
             "price": "",                       #必须
             "shipping": "配送",                  #必须
             "msrp":"可选的制造商建议零售价",
             "shipping_time": "时间",
             "main_image": "",                  
         }
        """

        func = "/variant/add"
        result = {}
        params_list = ["parent_sku", "sku", "inventory", "price", "shipping"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
        result = self.func_call(func, **params)
        return result

    def variant_retrieve(self, **params):
        """ 
            func: 想查看一个商品的状态
            :param params
            {
                "sku":"",
            }
        """
        func = "/variant"
        result =  {}
        params_list =  ["sku"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result

    def enable_variant_product(self, **params):
        """ 
            func: 让一个变体产品可用
            :param params
            {
                "sku" : "",
            }
        """
        func = "/variant/enable"
        result = {}
        params_list = ["sku"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result
    def disable_variant_product(self, **params):
        """ 
            func: 变体产品不可用 
            :param params
            {
                "sku": ""
            }
        """
        func = "/variant/disable"
        result = {}
        params_list = ["sku"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result



    def change_product_sku(self, **params):
        """ 
            func: 修改sku
            :param params
                {
                    "sku":"",
                    "new_sku": "",
                }
        """
        result = {}
        func = "/variant/change-sku"
        params_list  = ["sku", "new_sku"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result


    def update_inventory(self, **params):
        """ 
            func:  更新库存
            :param params
            {
                "sku": "",
                "inventory": "",
            }
        """
        result = {}
        func = "/variant/update-inventory"
        params_list = ["sku", "inventory"]
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result

    def list_all_variations(self, **params):
        """ 
            func: 列出所有变化的产品
            :param params
            {
                "start": "",
                "limit": "",
            }
        """
        func = "/variant/multi-get"
        result = {}
        params_list = ["start", "limit"]
        start, limit = 0, 15
        if params.get("start", ""): start = params.get("start")
        if params.get("limit", ""): limit = params.get("limit")
        params = {"start": start, "count": limit}
        tmp_result = self.func_call(func, **params)
        result = tmp_result
        while len(tmp_result.get("data", [])) >= limit:
            start += limit
            print "start: ", start
            tmp_result = self.func_call(func, **params)
            result.get("data").extend(tmp_result.get("data",[]))
            print "tmp_result: ", tmp_result
            time.sleep(0.5)
        return result

    #----------------------------------------------------------------------------
    #------------------------------上传一个图片  ----------------------------------
    def upload_image(self, **params):
        """ 
            func: 上传图片 
            :param params 
            {
                "image": "ABCD1234abcd", #Base64编码
            }
        """
        func = "/image"
        result = {}
        params_list = ["image"] 
        message = self.query_params(func, params_list, **params)
        if message:
            result["message"] = message
            return result
        result = self.func_call(func, **params)
        return result


    #----------------------------------------------------------------------------
    #------------------------------用户认证测试 --------------------------------
    def auth_test(self):
        func = "/auth_test"   #在前面要加 '/'
        req = self.func_call(func)
        print req






def main():
    store_list = STORE_DICT_LIST
    store_name = 'sandbox_001'
    print store_list[store_name]
    wish = Wish(store_list[store_name]['access_token'])

    wish.auth_test()
    """
    all_order_result = wish.fetch_all_order()
    print "all_order_result: ", all_order_result

    # 根据id取得订单
    params = {'id':'57242e8c0000000000000000'}
    one_order_result = wish.fetch_order_id(**params)
    print one_order_result


    #取消订单
    params = {'id': '5728230c0000000000000000', 'reason_code': 18}
    cancel_result = wish.cancel_order(**params)
    print cancel_result 


    #修改已装运订单的跟踪， 此订单为历史记录里面
    params =  {
            "id":"5722dd0c0000000000000000",    #order_id
            "tracking_provider": "USPS",
            "tracking_number": "12345678",   #快递号
            "ship_note": "给用户的注意",  #可以不填写这个参数
        }
    result = wish.modify_tracking(**params)
    print result


    # 标志为已发货
    params = {
        "id" : "57242e8c0000000000000000",
        "tracking_provider" : "USPS", 
        "tracking_number" : "12345678" ,
        }
    fulfile_result = wish.fulfile_one_order(**params)
    print fulfile_result
    """
    #-------------------------------------------------------------


    params =    {
             "name": "myshipping",                   #必须
             "description": "this is a cool shoe, it's very bueatiful!",           #必须
             "tags": "red, shoe, cool, myship",
             "parent_sku": "skudkjasfabcfc",                     #必须   #父sku，变体的产品必须
             "sku": "skudkjasfabcfc-red-22",                     #必须
             "color": "red",  #可选，部分没有
             "size": "22",   #可选
             "inventory": "100",                  #必须
             "price": "50",                       #必须
             "shipping": "10",                #必须
             "msrp":"50",
             "main_image": "https://dfk8hf9p19dtk.cloudfront.net/E/EL61365P6610-1.jpg",                  #必须
             "parent_sku": "parent-sku_manmansku", 
             "brand": "shipped",
             "landing_page_url": "https://dfk8hf9p19dtk.cloudfront.net/E/EL61365P6610-2.jpg",
             "upc": "abc123",
             "extra_images": "https://dfk8hf9p19dtk.cloudfront.net/E/EL61365P6610-3.jpg|https://dfk8hf9p19dtk.cloudfront.net/E/EL61365P6610-2.jpg",  #用了 '|' 分割
         }
#     result = wish.product_add(**params)
    result = wish.variant_add(**params)
    print result
    if result.get("code") == 0:
        if result.get("data").get("Product"):
            print "product_id:", result.get("data").get("Product").get("variants")[0].get("Variant").get("product_id")
        else:
            print "variation id:", result.get("data").get("Variant").get("product_id")
            print "current id: ", result.get("data").get("Variant").get("id")
    else:
        print "message: ", result.get("message")
    """
    ## 查看产品信息
    params = {"id": "572d9ebeae24f05a7962eee2", "parent_sku":"parent-sku"}
    result = wish.retrieve_product(**params)
    print result


    ## 更新产品信息
    params  = { 
                  "id": "572d9ebeae24f05a7962eee2",               #必须 
                  "parent_sku": "parent-sku",       #必须
                  "name": "产品名称",
                  "description": "it's new update description, color: red, size: 200*200",
                  "tags": "new, tags1, tags2",
                  "brand": "无牌子",
                  "landing_page_url": "http://img.alicdn.com/tps/TB1sNzAJFXXXXcDXpXXXXXXXXXX-1920-450.jpg",
                  "upc": "30",
                  "main_image": "http://img.alicdn.com/tps/TB1sNzAJFXXXXcDXpXXXXXXXXXX-1920-450.jpg",
                  "extra_images": "http://img.alicdn.com/tps/TB1sNzAJFXXXXcDXpXXXXXXXXXX-1920-450.jpg",
              }
    result = wish.update_product(**params)


    ## 列出所有产品信息
    result = wish.list_all_products()
    print result
    """

    ## 列出所有变更过的产品
    #result = wish.list_all_variations()
    #print result



if __name__ == "__main__":
#     main()
    code ='3ff343daafd847d980de7bbdd4b9bcab'
    client_id='5795739b09815726c88a47f0'
    client_secret='9e404f3916604fbcbd2f1d29eb078e31' 
    redirect_uri='https://localhost/'
    aa = Authorize()
    aa.get_token(code=code, client_id=client_id, client_secret = client_secret, redirect_uri=redirect_uri)

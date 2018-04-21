import React, {Component} from 'react';
import { Table, Popconfirm, message } from 'antd';
import { Link } from 'react-router-dom';

import '../style.less';

const data = [];
for (let i = 0; i < 100; i++) {
    data.push({
        key: i,
        Id: i,
        name: `Edrward ${i}`,
        type: '.cvs',
        storeName: "storeName",
        path: `London Park no. ${i}`,
        contractId: `NO.0123-${i}`,
        isPublic: "true",
        strategy: "field"
    });
}

class DataSourceList extends Component {
    onChangeStatus(id) {
        message.success("删除数据成功");
    }

    render() {
        const columns = [
            { title: '序号', width: 100, className: "dataTab", dataIndex: 'Id', key: 'Id', fixed: 'left' },
            { title: '名称', width: 150, className: "dataTab", dataIndex: 'name', key: 'name', fixed: 'left' },
            { title: '存储类型', className: "dataTab", dataIndex: 'type', key: 'type', width: 100 },
            { title: '存储名称', className: "dataTab", dataIndex: 'storeName', key: 'storeName', width: 200 },
            { title: '存储路径', className: "dataTab", dataIndex: 'path', key: 'path', width: 200 },
            { title: '合约ID', className: "dataTab", dataIndex: 'contractId', key: 'contractId', width: 200 },
            { title: '是否公开', className: "dataTab", dataIndex: 'isPublic', key: 'isPublic', width: 100 },
            { title: '策略', className: "dataTab", dataIndex: 'strategy', key: 'strategy', width: 200 },
            {
                title: '操作',
                key: 'operation',
                fixed: 'right',
                width: 250,
                render: () => (
                    <div>
                        <a href="">更新</a>
                        <Popconfirm title="是否删除?" onConfirm={() => this.onChangeStatus()} okText="是" cancelText="否">删除</Popconfirm>
                        <Link to="/dataSource/dictionary">字典</Link>
                    </div>
                )
            },
        ];        
        return (
            <Table columns={columns} dataSource={data} pagination={false} bordered={true} scroll={{ x: 1500, y: 600 }} />
        )
    }
}

export default DataSourceList;

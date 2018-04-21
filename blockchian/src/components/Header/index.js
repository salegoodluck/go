import React from 'react';
import { Link } from 'react-router-dom';
import { Icon, Avatar, Dropdown, Menu, Badge } from 'antd';

import './style.less';

// 用户logo下拉框内容
const profileMenu = (
    <Menu>
        <Menu.Item>
            <Link to='/UserCenter'>
                用户中心
            </Link>
        </Menu.Item>
        <Menu.Item>
            <Link to="/403">
                退出登录
            </Link>
        </Menu.Item>
    </Menu>    
);
// 信息下拉框
const noticeMenu = (notification) => {
    return (<Menu>
        {
            notification.length > 0
                ? notification.map(item => (
                    <Menu.Item key={item.id}>
                        <Link to={`/userCenter/msgCenter/${item.id}`} >{item.msg}</Link>
                    </Menu.Item>
                ))
                : <Menu.Item key="empty">没有信息</Menu.Item>
        }
    </Menu>)
}

class Header extends React.Component {
    static defaultProps = {
        notification: []
    }

    render() {
        // const { notification } = this.props;
        const notification = [
            {id:1,msg:"数据请求和数据提供的消息通知1"},
            {id:2,msg:"数据请求和数据提供的消息通知2"},
            {id:3,msg:"数据请求和数据提供的消息通知3"},
            {id:4,msg:"数据请求和数据提供的消息通知4"},
            {id:5,msg:"数据请求和数据提供的消息通知5"},
            {id:6,msg:"数据请求和数据提供的消息通知6"},
        ];
        return (
            <header>
                <div className="logo" to='/'>
                    <img src="" alt="" />
                    <div className="company">
                        <h3>信工厂</h3>
                        <h4 className="companyIntro">帮助企业进行数据交流</h4>
                    </div>
                </div>
                <div className="user">
                    <Dropdown overlay={noticeMenu(notification)} placement="bottomRight">
                        <div className="notice">
                            <Badge count={notification.length} overflowCount={99}>
                                <Icon type="bell" style={{ fontSize: '1.2rem' }} />
                            </Badge>
                        </div>
                    </Dropdown>            
                    <Avatar style={{ marginRight: 8 }} icon="user" />
                    <Dropdown overlay={profileMenu}>
                        <span className="profile">
                            <span>武必成</span>
                            <Icon type="down" />
                        </span>
                    </Dropdown>
                </div>
            </header>
        )        
    }
}

export default Header
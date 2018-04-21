import React from 'react';
import { Icon } from 'antd';

import Card from './Components/Card';
import Banner from './Components/Banner';

import '../Home/style.less';

const bannerInfo = [
    {
        id: 1,
        image: 'http://4.su.bdimg.com/skin/12.jpg',
        info: '向市场提供安全、高效的数据融合的综合解决方案',
        name: '信工厂，帮助企业数据交流'
    }, {
        id: 2,
        image: 'http://4.su.bdimg.com/skin/2.jpg',
        info: '向市场提供安全、高效的数据融合的综合解决方案',
        name: '试金石信用'
    }
];

const entries = [{
        title: "数据字典",
        description: "企业内部保留的相关数据源",
        color: "#3d85c6",
        icon: <Icon type="database" />,
        href: "/dataSource"
    }, {
        title: "数据需求",
        description: "发布数据的需求、解决数据缺乏难点",
        color: "#e15151",
        icon: <Icon type="notification" />,
        href: "/dataTask"
    }, {
        title: "数据提供",
        description: "查看需求，为其它企业提供数据帮助",
        color: "#6aa84f",
        icon: <Icon type="export" />,
        href: "/dataProvide"
    }, {
        title: "用户设置",
        description: "企业相关信息中心和消息中心",
        color: "#3d85c6",
        icon: <Icon type="setting" />,
        href: "/userCenter/setting"
    },
];

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <main className="home">
                <Banner bannerInfo={bannerInfo}/>
                <article>
                    <h3>基础功能</h3>
                    <section>
                        {entries.map((item, index) =>
                            <Card key={index} cardContent={item} />
                        )}
                    </section>
                </article>
            </main>
        )
    }
}

export default Home;
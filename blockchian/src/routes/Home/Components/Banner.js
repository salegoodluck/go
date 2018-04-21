import React from "react";
import { Carousel } from 'antd';

import '../style.less';

const Banner = (props) => {
    return (
        <div className="banner">
            <Carousel autoplay>
                {
                    props.bannerInfo.map((item) =>
                        <div className="bannerWrap" key={item.id} style={{ background: `url(${item.image})` }}>
                            <div className="bannerBox">
                                <p className="title">{item.name}</p>
                                <p className="description">{item.info}</p>
                            </div>
                        </div>
                    )
                }
            </Carousel>
        </div>
    )
}

export default Banner;

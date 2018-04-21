import React from 'react';
// import { Card } from 'antd';
import { Link } from 'react-router-dom';

import "../style.less";

const Card = (props) => {
    const cardInfo = props.cardContent;
    return (
        <Link className="cardLink" to={props.cardContent.href}>
            <div className="cardWrap">
                <div className="cardIcon" style={{color: cardInfo.color}}>
                    {cardInfo.icon}
                </div>
                <div className="cardContent">
                    <p className="cardTit">{cardInfo.title}</p>
                    <p className="cardDes">{cardInfo.description}</p>
                </div>
            </div>
        </Link>
    )
}

export default Card;
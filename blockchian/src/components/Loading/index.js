import React from 'react'
import { Spin } from 'antd'
import './style.less'

const Loading = ({ isLoading, error }) => {
    // Handle the loading state
    if (isLoading) {
        return (
            <div className="loading">
                <Spin size="large" tip="加载中..." />
            </div>
        )
    }
    // Handle the error state
    else if (error) {
        return <div className="loading">Sorry, there was a problem loading the page.</div>;
    }
    else {
        return null;
    }
};

export default Loading;

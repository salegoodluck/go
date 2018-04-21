import React from 'react';

import Header from '../Header';
import Footer from '../Footer';

import './style.less';

class Wrapper extends React.Component {
    render() {
        const { children } = this.props;
        return (
            <div className="wrapper">
                <Header/>
                <div className="space"></div>
                {children}
                <Footer className="footer"/>
            </div>
        )
    }
}

export default Wrapper;
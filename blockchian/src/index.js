import React from 'react';
import ReactDOM from 'react-dom';
// import { Provider } from "mobx-react";

import 'antd/dist/antd.css';
import './assets/styles/base.less';

import App from './routes';

ReactDOM.render(
    // <Provider>
    //     <App/>
    // </Provider>, 
    <App />,
    document.getElementById('root')
);

import React from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import Theme, { getTheme } from 'react-uwp/Theme';
import Loadable from 'react-loadable';

import history from './history';
import Wrapper from '../components/wrapper';
import Loading from '../components/Loading';

// 路由按需加载
// Loadable中loading为必须属性
const Home = Loadable({
    loader: () => import("./Home"),
    loading: Loading
});
const DataSource = Loadable({
    loader: () => import("./DataSource"),
    loading: Loading
});
const Dictionary = Loadable({
    loader: () => import("./Dictionary"),
    loading: Loading
});
/* const DataTask = Loadable({
    loader: () => import("./DataTask"),
    loading: Loading
});
const DataProvide = Loadable({
    loader: () => import("./DataProvide"),
    loading: Loading
});
const UserCenter = Loadable({
    loader: () => import("./UserCenter"),
    loading: Loading
}); */

// const routes = [
//     {
//         path: "/",
//         component: Home
//     },
//     {
//         path: "/home",
//         component: Home
//     },
//     {
//         path: "/dataSource",
//         component: DataSource,
//         routes: [
//             {
//                 path: "/dataSource/dictionary",
//                 component: Dictionary
//             }
//         ]
//     },
// ];

// const RouteComponent = (route, childProps) => (
    
//     <Route path={route.path} props={childProps} render={props => (
//         // pass the sub-routes down to keep nesting
//         <route.component {...props} routes={route.routes} />
//     )} />
// )

export default ({ childProps }) => (
    <Router history={history}>
        <Theme style={{ backgroundColor: '#f5f5f5', fontFamily: '' }} theme={getTheme({ themeName: 'light', accent: '#108EE9' })}>
            <Wrapper>
                <Switch>
                    {/* routes.map((route, i) => (
                        <RouteComponent key={i} {...route} childProps={childProps} />
                    )) */}
                    <Route path="/" exact component={Home} props={childProps} />
                    <Route path="/home" exact component={Home} props={childProps} />
                    <Route path="/dataSource" exact component={DataSource} props={childProps}/>>
                    {/* 
                    <Route path="/dataTask" exact component={DataTask} props={childProps} />
                    <Route path="/dataProvide" exact component={DataProvide} props={childProps} />
                    <Route path="/userCenter" exact component={UserCenter} props={childProps} /> */}
                </Switch>
            </Wrapper>
        </Theme>
    </Router>
)

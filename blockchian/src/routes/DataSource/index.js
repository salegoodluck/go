import React ,{ Component } from 'react';
import { Input, Select, Button} from 'antd';

import DataSourceList from './components/dataSourceList';
import './style.less';

// const Search = Input.Search;
// const Option = Select.Option;

class DataSource extends Component {
    render() {
        return (
            <main className="dataSource">
                <p className="dictTitle">数据源列表</p>
                <section>
                    <div className="operation">
                        <Button className="addData" type="primary">添加数据源</Button>
                    </div>
                    <DataSourceList />                
                </section>
            </main>
        )
    }
}

export default DataSource;

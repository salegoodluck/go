import React, { Components } from 'react';
import { Input, Select, Button } from 'antd';

import './style.less';

// const Search = Input.Search;
// const Option = Select.Option;

class Dictionary extends Components {
    render() {
        return (
            <main className="dataSource">
                <p className="dictTitle">数据字典列表</p>
                <section>
                    <div className="operation">
                        <Button className="addData" type="primary">添加字典</Button>
                    </div>

                </section>
            </main>
        )
    }
}

export default Dictionary;

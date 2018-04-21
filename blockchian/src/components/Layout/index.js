import React from 'react';
import Loading from '../Loading';
import Wrapper from '../wrapper';

import styles from './style.less';

function Layout({
    loading = false,
    children
}) {
    return (
        <div className={styles.app}>
            <Wrapper>
                <div className={styles.content}>
                    {children && !loading ? children : <Loading />}
                </div>
            </Wrapper>
        </div>
    )
}

export default Layout

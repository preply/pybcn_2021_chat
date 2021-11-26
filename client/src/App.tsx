import * as React from 'react';
import { Router } from './routes/router';
import styles from './app.module.scss';

export const App = () => (
    <div className={styles.container}>
        <Router />
    </div>
);

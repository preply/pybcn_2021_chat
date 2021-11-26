import * as React from 'react';
import { Router } from './routes/router';
import { useEffect } from 'react';
import { getUser } from './api/user.api';
import { useDispatch } from 'react-redux';
import { setUser } from './store/core/core.actions';
import styles from './app.module.scss';

export const App = () => {
    const dispatch = useDispatch();

    const getUserData = async () => {
        const user = await getUser();
        !!user && dispatch(setUser(user));
    };

    useEffect(() => {
        getUserData();
    }, [dispatch, getUserData]);

    return (
        <div className={styles.container}>
            <Router />
        </div>
    );
};

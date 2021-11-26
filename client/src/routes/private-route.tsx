import React, { ReactNode, ReactNodeArray } from 'react';
import { Navigate } from 'react-router-dom';
import { Routes } from './routes.types';
import { LocalStorage } from '../models/localstorage';

type RouteProps = {
    children?: ReactNode | ReactNodeArray;
    [rest: string]: unknown;
};
export const PrivateRoute = ({ children, ...rest }: RouteProps) => {
    const user = localStorage.getItem(LocalStorage.USER);

    if (!user) {
        return <Navigate to={Routes.LOGIN} />;
    }

    const childrenWithProps = React.Children.map(children, child => {
        if (React.isValidElement(child)) {
            return React.cloneElement(child, { ...rest });
        }
        return child;
    });

    return <div>{childrenWithProps}</div>;
};

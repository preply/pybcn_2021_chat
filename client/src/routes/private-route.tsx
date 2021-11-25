import React, { ReactNode, ReactNodeArray } from 'react';
import { Navigate } from 'react-router-dom';
import { Routes } from './routes.types';

type RouteProps = {
    children?: ReactNode | ReactNodeArray;
    [rest: string]: unknown;
};
export const PrivateRoute = ({ children, ...rest }: RouteProps) => {
    const user = null;

    if (!user) {
        return <Navigate to={Routes.LOGIN} />;
    }

    const childrenWithProps = React.Children.map(children, child => {
        // Checking isValidElement is the safe way and avoids a typescript
        // error too.
        if (React.isValidElement(child)) {
            return React.cloneElement(child, { ...rest });
        }
        return child;
    });

    return <div>{childrenWithProps}</div>;
};

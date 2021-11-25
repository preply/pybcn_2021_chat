import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import { Routes as RoutesTypes } from './routes.types';
import { Error404 } from '../components/404/error-404';
import { PrivateRoute } from './private-route';
import Chat from '../pages/Chat';
import Login from '../pages/Login';
import Register from '../pages/Register';

export const Router = () => (
    <Routes>
        <Route path="/" element={<Navigate replace to={RoutesTypes.CHAT} />} />
        <Route path={RoutesTypes.LOGIN} element={<Login />} />
        <Route path={RoutesTypes.REGISTER} element={<Register />} />
        <Route path={RoutesTypes.REGISTER} element={<Register />} />
        <Route
            path={RoutesTypes.CHAT}
            element={
                <PrivateRoute>
                    <Chat />
                </PrivateRoute>
            }
        />
        <Route path="*" element={<Error404 />} />
    </Routes>
);

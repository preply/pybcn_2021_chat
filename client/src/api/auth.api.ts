import { axiosInstance } from './axios-instance';
import { User } from '../models/user';

export const register = (name: string, password: string, lang: string): Promise<User> =>
    axiosInstance.post('/users/register', { name, password, lang });

export const login = (name: string, password: string): Promise<User> =>
    axiosInstance.post('/users/login', { name, password });

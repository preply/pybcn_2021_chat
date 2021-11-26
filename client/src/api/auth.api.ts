import { axiosInstance } from './axios-instance';
import { User } from '../models/user';

export const register = (name: string, lang: string): Promise<User> =>
    axiosInstance.post('/users/register', { name, lang });

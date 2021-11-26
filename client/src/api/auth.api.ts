import { axiosInstance } from './axios-instance';
import { User } from '../models/user';

export const register = (name: string, lang: string): Promise<{ data: User }> =>
    axiosInstance.post('/users/register', { name, lang });

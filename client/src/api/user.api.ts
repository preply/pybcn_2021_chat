import { axiosInstance } from './axios-instance';
import { User } from '../models/user';

export const getUser = (): Promise<User> => axiosInstance.get('/users/me');

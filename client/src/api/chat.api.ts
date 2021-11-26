import { axiosInstance } from './axios-instance';
import { Room } from '../models/room';

export const getChats = (): Promise<Room[]> => axiosInstance.get('/rooms');

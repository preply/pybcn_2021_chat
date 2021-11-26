import { axiosInstance } from './axios-instance';
import { Room } from '../models/room';

export const getChats = (): Promise<Room[]> =>
    axiosInstance.get<{ results: Room[] }>('/rooms').then(res => res.data.results);
export const getChat = (roomId: string, userId: string): Promise<Room> =>
    axiosInstance.get(`/rooms/${roomId}/${userId}`).then(res => res.data);

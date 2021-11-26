import axios from 'axios';

export const axiosInstance = axios.create({
    headers: {
        'Content-Type': 'application/json',
    },
    baseURL: 'http://localhost:5000/api',
    withCredentials: true,
});

axiosInstance.interceptors.response.use(
    res => res.data,
    error => {
        return Promise.reject(error);
    },
);

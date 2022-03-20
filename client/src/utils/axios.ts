import axios from 'axios';
import { config } from '../config/config';

export const axiosInstance = axios.create({
    baseURL: config.backendUrl || 'http://localhost:8001',
    withCredentials: true
});

axiosInstance.interceptors.request.use((config) => {
    const authKey = localStorage.getItem('token');
    if (!authKey) {
        // nothing to handle
    }
    if (config.headers) config.headers.authorization = `Bearer ${authKey}`;
    return config;
});

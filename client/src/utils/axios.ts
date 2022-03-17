import axios from 'axios';
import { config } from '../config/config';

export const axiosInstance = axios.create({
    baseURL: config.backendUrl || 'http://localhost:8001',
    withCredentials: true
});

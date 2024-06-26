import axios from 'axios';

const API_BASE_URL = 'http://localhost:4000'; // Update with your actual backend URL

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add the token to headers if available
apiClient.interceptors.request.use(async (config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Response interceptor to handle token refresh on 401 errors
apiClient.interceptors.response.use((response) => {
    return response;
}, async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
            const refreshToken = localStorage.getItem('refreshToken');
            const { data } = await apiClient.post('/auth/refresh-token', { token: refreshToken });
            localStorage.setItem('token', data.accessToken);
            originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
            return apiClient(originalRequest);
        } catch (err) {
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            window.location.href = '/login'; // Redirect to login page
            return Promise.reject(err);
        }
    }
    return Promise.reject(error);
});

// Function to login user
export const loginUser = async (username, password) => {
    try {
        const response = await apiClient.post('/auth/login', { username, password });
        localStorage.setItem('token', response.data.accessToken);
        localStorage.setItem('refreshToken', response.data.refreshToken);
        return response.data;
    } catch (error) {
        console.error('Error logging in:', error);
        throw error;
    }
};

// Function to signup user
export const signupUser = async (username, email, password) => {
    try {
        const response = await apiClient.post('/auth/signup', { username, email, password });
        return response.data;
    } catch (error) {
        console.error('Error signing up:', error);
        throw error;
    }
};

// Function to fetch backtest results
export const fetchBacktestResults = async (startDate, endDate, selectedCoin, initialCash, smwValue, fmwValue, stakeValue) => {
    try {
        const response = await apiClient.post('/backtest', { startDate, endDate, selectedCoin, initialCash, smwValue, fmwValue, stakeValue });
        return response.data;
    } catch (error) {
        console.error('Error fetching backtest results:', error);
        throw error;
    }
};

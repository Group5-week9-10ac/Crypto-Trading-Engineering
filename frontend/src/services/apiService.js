import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to fetch backtest results
export const fetchBacktestResults = async (requestData) => {
  try {
    const token = localStorage.getItem('token');
    const response = await apiClient.post('/api/backtest', requestData, {
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Function to log in user
export const loginUser = async (username, password) => {
  try {
    const response = await apiClient.post('/api/auth/login', {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Function to sign up user (add this function)
export const signupUser = async (username, email, password) => {
  try {
    const response = await apiClient.post('/api/auth/signup', {
      username,
      email,
      password,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};


import axios from 'axios';

const API = axios.create({
    baseURL: 'http://localhost:3000/api', // Adjust this URL if your backend runs on a different port
});

export default API;
import axios from 'axios';

const BASE_URL = 'http://your-api-base-url.com'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = async (usernameOrEmail, password) => {
  try {
    const requestData = {
      action: 'login',
      data: {
        username_or_email: usernameOrEmail,
        password: password,
      },
    };

    const response = await api.post('/api/common/user?action=login', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (username, password, email) => {
  try {
    const requestData = {
      action: 'register',
      data: {
        username: username,
        password: password,
        email: email,
      },
    };

    const response = await api.post('/api/common/user?action=register', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const validateCode = async (code) => {
  try {
    const requestData = {
      action: 'valid',
      data: {
        code: code,
      },
    };

    const response = await api.post('/api/common/user?action=valid', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

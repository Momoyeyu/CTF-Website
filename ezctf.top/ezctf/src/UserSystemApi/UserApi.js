import axios from 'axios';

const BASE_URL = 'http://your-api-base-url.com'; // 替换为实际的API基础URL

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

export const login = async (usernameOrEmail, password) => {
  try {
    const response = await api.post('/api/common/user?action=login', {
      action: 'login',
      data: {
        username_or_email: usernameOrEmail,
        password: password,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (username, password, email) => {
  try {
    const response = await api.post('/api/common/user?action=register', {
      action: 'register',
      data: {
        username: username,
        password: password,
        email: email,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const validateCode = async (code) => {
  try {
    const response = await api.post('/api/common/user?action=valid', {
      action: 'valid',
      data: {
        code: code,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
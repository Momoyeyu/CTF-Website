import axios from 'axios';
axios.defaults.withCredentials = true;
const BASE_URL = 'http://localhost:80'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = async (usernameOrEmail, password1) => {
  try {
    const requestData = {
      action: "login",
      data: {
        username_or_email: usernameOrEmail,
        password: password1,
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

export const modifyUserInfo = async (old_username,new_username,password) => {
  try {
    const requestData = {
      action: 'modify_user_info',
      data: {
        old_username: old_username,
        new_username: new_username,
        password: password
      },
    };
    const response = await api.put('/api/common/user?action=modify_user_info', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const logoutUser = async () => {
  try {
    const requestData = {
      action: 'logout',
    };

    const response = await api.get('/api/common/user?action=logout', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteUserInfo = async (password) => {
  try {
    const requestData = {data:{
      action: 'del_account',
      data: {
        password: password
      },
    }};

    const response = await api.delete('/api/common/user?action=del_account', requestData);
    return response.status;
  } catch (error) {
    throw error;
  }
};

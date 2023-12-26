import axios from 'axios';
axios.defaults.withCredentials = true;
const BASE_URL = 'http://8.130.98.1:8080'; 

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

export const validateCode = async (username, valid_code) => {
  try {
    const requestData = {
      action: 'user_active',
      data: {
        username: username,
        valid_code: valid_code,
      },
    };

    const response = await api.post('/api/common/user?action=user_active', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const forgetPassword = async (email) => {
  try {
    const requestData = {
      action: 'forget_password',
      data: {
        email: email,
      },
    };

    const response = await api.post('/api/common/user?action=forget_password', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const resetPassword = async (valid_code,email,new_password) => {
  try {
    const requestData = {
      action: 'reset_password',
      data: {
        valid_code: valid_code,
        email: email,
        new_password: new_password,
      },
    };

    const response = await api.put('/api/common/user?action=reset_password', requestData);
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

export const profile = async (username) => {
  try {
    const response = await api.get(`/api/common/user?action=profile&username=${username}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const user_profile = async () => {
  try {
    const response = await api.get(`/api/common/user?action=update_profile`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
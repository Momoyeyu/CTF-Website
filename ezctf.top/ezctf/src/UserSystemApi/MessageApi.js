import axios from 'axios';
axios.defaults.withCredentials = true;
const BASE_URL = 'http://localhost:80'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getMessage = async () => {
    try {
      const response = await api.get(`/api/common/message?action=get_messages`);
      return response.data;
    } catch (error) {
      throw error;
    }
};

export const getApply = async () => {
  try {
    const response = await api.get(`/api/common/message?action=get_applications`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const checkMessage = async () => {
    try {
      const response = await api.get(`/api/common/message?action=check_messages`);
      return response.data;
    } catch (error) {
      throw error;
    }
};
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getFairRecommendation = async (query, kecamatan = '') => {
  try {
    const params = { query };
    if (kecamatan) {
      params.kecamatan = kecamatan;
    }
    const response = await apiClient.get('/route/fair-recommendation', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching fair recommendation:', error);
    throw error;
  }
};

export const getDestinations = async (kecamatan = '', limit = 10) => {
  try {
    const params = { limit };
    if (kecamatan) {
      params.kecamatan = kecamatan;
    }
    const response = await apiClient.get('/destinasi', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching destinations:', error);
    throw error;
  }
};

export const sendChatMessage = async (message, history = []) => {
  try {
    const response = await apiClient.post('/chat', { message, history });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

// frontend/src/services/apiService.ts
import axios from 'axios';
import { PerformanceAnalysisRequestData, PerformanceAnalysisResponseData } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchPerformanceAnalysis = async (
  data: PerformanceAnalysisRequestData
): Promise<PerformanceAnalysisResponseData> => {
  try {
    const response = await apiClient.post('/analysis/performance', data);
    return response.data;
  } catch (error) {
    console.error('Error fetching performance analysis:', error);
    // You might want to throw a more specific error or handle it
    throw error;
  }
};
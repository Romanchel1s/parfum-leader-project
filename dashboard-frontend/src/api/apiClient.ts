import axios from 'axios';
import mockApi from './mocks';

// Toggle between real and mock APIs
const USE_MOCK_API = false;
const baseUrl = import.meta.env.VITE_API_BASE_URL;

const apiClient = axios.create({
  baseURL: baseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

const api = {
  getEmployeeMessages: (employeeId: string) =>
    USE_MOCK_API
      ? mockApi.getEmployeeMessages(employeeId)
      : apiClient.get(`/employees/${employeeId}/messages`).then(res => res.data),

  updateProductFrequency: (frequency: string) =>
    USE_MOCK_API
      ? mockApi.updateProductFrequency(frequency)
      : apiClient.put('/products/frequency', { frequency }).then(res => res.data),

  getProductInfo: (startDate?: string, endDate?: string) =>
    USE_MOCK_API
      ? mockApi.getProductInfo(startDate, endDate)
      : apiClient
          .post('/products/info', { startDate, endDate })
          .then(res => res.data),

  getStoreEmployees: (storeId: string) =>
    USE_MOCK_API
      ? mockApi.getStoreEmployees(storeId)
      : apiClient.get(`/stores/${storeId}/employees`).then(res => res.data),

  getEmployeeSchedule: (employeeId: string) =>
    USE_MOCK_API
      ? mockApi.getEmployeeSchedule(employeeId)
      : apiClient
          .get(`/employees/${employeeId}/Attendance`)
          .then(res => res.data),
  getAllProducts: () => 
    apiClient.get('/product/all_products').then(res => res.data),

  getAllStores: async () => {
    const response = await fetch('/api/upload/bot/map.json');
    if (!response.ok) {
    throw new Error('Network response was not ok');
    }
    const jsonData = await response.json();
    const stores = jsonData.map((store: { id: unknown; name: unknown; }, index: unknown) => ({
        id: store.id || index,
        name: store.name || 'unknown',
    }));
    return stores
  },
  getStoreAttendanceStats: async(storeId: string, startTime: string, endTime: string) => {
    return apiClient.get(`/stores/${storeId}/attendance_stat/${startTime}/${endTime}`).then(res => res.data)
  },
  getStoresAttendance: async(startTime: string, endTime: string) => {
    return apiClient.get(`/stores/nearest/${startTime}/${endTime}`).then(res => res.data)
  },
  getProductsByTime:(storeId: string, startTime: string, endTime: string) =>
    apiClient.get(`/stores/${storeId}/products/products_available/${startTime}/${endTime}`).then(res => res.data),
  getProduct: (id: string) => apiClient.get(`/product/${id}`).then(res => res.data),
  updateStoreCheckSettings: (storeId: string, settings: { daily_checks_count: number; daily_checks_interval: number; }) =>
    apiClient.put(`/stores/${storeId}/update_daily_checks`, settings).then(res => res.data),
};

export default api;


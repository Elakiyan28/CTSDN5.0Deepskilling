import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  headers: { "Content-Type": "application/json" },
  timeout: 5000,
});

// Request interceptor: attach auth header to every outgoing request
apiClient.interceptors.request.use((config) => {
  const mockToken = "mock-jwt-token";
  config.headers.Authorization = `Bearer ${mockToken}`;
  return config;
});

// Response interceptor: unwrap data, standardise errors
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response?.status ?? 0;
    const message = error.response?.data?.message || error.message || "Unknown API error";
    const standardError = new Error(message);
    standardError.statusCode = statusCode;
    return Promise.reject(standardError);
  }
);

export default apiClient;

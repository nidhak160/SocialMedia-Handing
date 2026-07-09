import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    const refresh = localStorage.getItem("refresh");

    if (!refresh) {
      localStorage.clear();
      window.location.href = "/";
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/refresh/", {
        refresh,
      });

      localStorage.setItem("access", response.data.access);
      originalRequest.headers.Authorization = `Bearer ${response.data.access}`;

      return api(originalRequest);
    } catch (refreshError) {
      localStorage.clear();
      window.location.href = "/";
      return Promise.reject(refreshError);
    }
  }
);

export default api;

import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  timeout: 10000,
  headers: {
    Accept: "application/json",
  },
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

    if (
      error.response?.status !== 401 ||
      originalRequest._retry
    ) {
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
      const res = await axios.post(
        "http://127.0.0.1:8000/api/auth/refresh/",
        {
          refresh,
        }
      );

      localStorage.setItem("access", res.data.access);

      originalRequest.headers.Authorization =
        `Bearer ${res.data.access}`;

      return api(originalRequest);
    } catch (err) {
      localStorage.clear();
      window.location.href = "/";
      return Promise.reject(err);
    }
  }
);

export default api;
import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/";

const apiService = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ✅ Attach access token to every request
apiService.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ Refresh token if access token expires
apiService.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem("refresh");
      if (!refresh) {
        console.error("No refresh token available. Logging out.");
        logout();
        return Promise.reject(error);
      }

      try {
        // Request a new access token
        const { data } = await axios.post(`${API_BASE_URL}token/refresh/`, { refresh });
        localStorage.setItem("access", data.access);

        // Retry original request with new token
        error.config.headers.Authorization = `Bearer ${data.access}`;
        return apiService(error.config);
      } catch (refreshError) {
        console.error("Refresh token invalid. Logging out.");
        logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// ✅ Logout function (clears tokens and redirects)
const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("username");
  window.location.href = "/login"; // Redirect to login page
};

export default apiService;

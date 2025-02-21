import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api"; // Adjust if needed

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Function to log in
export const loginUser = async (username, password) => {
  try {
    const response = await api.post("/login/", { username, password });
    return response.data; // Returns { access, refresh }
  } catch (error) {
    console.error("Login failed", error);
    throw error;
  }
};

export const refreshToken = async () => {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return null;
  
    try {
      const response = await axios.post(`${API_BASE_URL}token/refresh/`, { refresh });
      localStorage.setItem("access", response.data.access); // Update token
      return response.data.access;
    } catch (error) {
      console.error("Token refresh failed:", error);
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      return null;
    }
  };

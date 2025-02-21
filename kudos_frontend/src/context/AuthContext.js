import React, { createContext, useState, useEffect } from "react";
import { loginUser, refreshToken } from "../api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("access") || null);

  useEffect(() => {
    if (token) {
      setUser({
        username: localStorage.getItem("username"),
        email: localStorage.getItem("email"),
        organization: JSON.parse(localStorage.getItem("organization")),
      });
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const data = await loginUser(username, password);

      // Store tokens
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      // Store user info
      localStorage.setItem("username", data.user.username);
      localStorage.setItem("email", data.user.email);
      localStorage.setItem("organization", JSON.stringify(data.user.organization));

      setToken(data.access);
      setUser({
        username: data.user.username,
        email: data.user.email,
        organization: data.user.organization,
      });
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
    localStorage.removeItem("email");
    localStorage.removeItem("organization");
    
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;

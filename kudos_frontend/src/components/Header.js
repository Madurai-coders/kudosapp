import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";
import apiService from "../services/apiService";
import { capitalizeFirstLetter } from "../Utility/stringUtils";
const Header = () => {
  const { user, logout } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem("refresh"); // Get stored refresh token
      logout(); // Clear user context
      await apiService.post("/logout/", { refresh_token: refreshToken });
      window.location.href = "/"; // Redirect to login
    } catch (error) {
      console.error("Logout failed", error);
    }
  };


  return (
    <header className="bg-gray-900 text-white  px-2 flex justify-between items-center shadow-lg">
      {/* Left: Welcome Message */}
      <h1 className="text-xl font-semibold">
        Welcome, <span className="text-blue-400">{capitalizeFirstLetter(user?.username)}
        </span>! 🎉
      </h1>

      {/* Right: Logout Button */}
      <button
        onClick={handleLogout}
        className="bg-red-600 hover:bg-red-700 p-1 m-2 mt-3 pt-0 rounded-full transition-all"
      >
        <span className="text-white text-xl">⏻</span> {/* Power Icon */}
      </button>
    </header>
  );
};

export default Header;

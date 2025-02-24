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
    <header className="bg-gray-900 text-white px-2 flex justify-between items-center shadow-lg">
    {/* Left: Welcome Message */}
    <h1 className="text-xl font-semibold">
      Welcome, <span className="text-blue-400">{capitalizeFirstLetter(user?.username)}</span>! 🎉
    </h1>
  
    {/* Right: Organization & Logout Button */}
    <div className="flex items-center space-x-4">
      {/* Organization Name */}
      {user?.organization && (
        <span className="text-sm text-gray-300">
          Organization: <span className="text-green-400 font-semibold">{user.organization?.name}</span>
        </span>
      )}
  
      {/* Logout Button */}
      <button
  onClick={handleLogout}
  className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition-all duration-300 transform hover:scale-105 active:scale-95 m-2 pt-1"
>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={2}
    stroke="currentColor"
    className="w-6 h-6"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v15A2.25 2.25 0 007.5 22.5h6a2.25 2.25 0 002.25-2.25V15M9 12h12m0 0l-3-3m3 3l-3 3"
    />
  </svg>
  <span>Logout</span>
</button>

    </div>
  </header>
  
  );
};

export default Header;

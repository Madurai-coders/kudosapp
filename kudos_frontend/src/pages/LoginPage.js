import React, { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate("/kudos"); // Redirect after login
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-black">
      {/* 🎉 Background Floating Emojis */}
      <div className="absolute inset-0 overflow-hidden">
  {/* Top Floating Emojis */}
  <div className="absolute top-5 left-10 text-6xl animate-bounce">🎉</div>
  <div className="absolute top-10 right-20 text-5xl animate-spin">👏</div>
  <div className="absolute top-16 left-1/3 text-4xl animate-pulse">🎊</div>
  <div className="absolute top-10 right-1/4 text-7xl animate-bounce">🥳</div>
  <div className="absolute top-20 left-3/4 text-3xl animate-spin">💫</div>

  {/* Mid Floating Emojis */}
  <div className="absolute top-1/4 left-5 text-6xl animate-pulse">🙌</div>
  <div className="absolute top-1/3 right-10 text-5xl animate-spin">🔥</div>
  <div className="absolute top-1/2 left-1/3 text-8xl animate-bounce">🏆</div>
  <div className="absolute top-1/2 right-1/4 text-4xl animate-pulse">💪</div>
  <div className="absolute top-1/3 left-1/4 text-7xl animate-spin">🌟</div>
  <div className="absolute top-1/3 right-1/3 text-6xl animate-bounce">🎯</div>
  <div className="absolute top-1/2 left-10 text-5xl animate-pulse">💥</div>
  <div className="absolute top-1/2 right-5 text-3xl animate-spin">🚀</div>

  {/* Bottom Floating Emojis */}
  <div className="absolute bottom-10 left-1/3 text-7xl animate-bounce">🎶</div>
  <div className="absolute bottom-5 right-1/4 text-6xl animate-spin">💖</div>
  <div className="absolute bottom-16 left-10 text-5xl animate-pulse">🥂</div>
  <div className="absolute bottom-8 right-5 text-4xl animate-bounce">🎁</div>
  <div className="absolute bottom-12 left-1/5 text-6xl animate-spin">🕺</div>
  <div className="absolute bottom-3 right-1/3 text-5xl animate-pulse">✨</div>
  <div className="absolute bottom-15 left-2/3 text-8xl animate-bounce">🎵</div>
  <div className="absolute bottom-20 right-10 text-7xl animate-spin">🏅</div>
  <div className="absolute bottom-25 left-12 text-3xl animate-pulse">🌈</div>
  <div className="absolute bottom-30 right-1/5 text-4xl animate-bounce">💎</div>
</div>


      {/* 🌑 Login Card */}
      <div className="relative bg-gray-900 bg-opacity-80 backdrop-blur-lg p-8 rounded-2xl shadow-lg w-full max-w-md border border-gray-700">
        <h2 className="text-3xl font-bold mb-6 text-center text-white">
          👏 Kudos App
        </h2>
        
        {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Username:
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Password:
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
          </div>
          
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-transform transform hover:scale-105"
          >
            🚀 Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;

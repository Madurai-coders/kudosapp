import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Kudos from "./pages/KudosPage";
import Login from "./pages/LoginPage";
import ProtectedRoute from "./components/ProtectedRoute";
import { useContext } from "react";
import AuthContext from "./context/AuthContext";
import "./index.css";

function App() {
  return (
    <AuthProvider> {/* Ensure AuthContext is wrapped at the top level */}
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<AuthWrapper />} />
            <Route path="/kudos" element={<ProtectedRoute><Kudos /></ProtectedRoute>} />
            <Route path="*" element={<AuthWrapper />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

// A wrapper component to use useContext safely inside Routes
const AuthWrapper = () => {
  const { user } = useContext(AuthContext);
  return user ? <Navigate to="/kudos" /> : <Login />;
};

export default App;

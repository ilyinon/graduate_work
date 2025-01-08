import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <Routes>
        {/* Маршруты */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard/*" element={<ProtectedRoute element={<Dashboard />} />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

function ProtectedRoute({ element }) {
  const isAuthenticated = !!localStorage.getItem('token');
  return isAuthenticated ? element : <Navigate to="/login" />;
}

export default App;

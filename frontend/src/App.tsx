import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import ThemeProvider from './contexts/ThemeContext';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import BiometricLoginPage from './pages/BiometricLoginPage';
import BiometricTestPage from './pages/BiometricTestPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import UserDashboardPage from './pages/UserDashboardPage';

// Components
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';

// Global styles
import './index.css';

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Box sx={{ 
            minHeight: '100vh',
            background: 'background.default',
            fontFamily: 'body1.fontFamily',
          }}>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/biometric-login" element={<BiometricLoginPage />} />
              <Route path="/biometric-test" element={<BiometricTestPage />} />
              <Route path="/admin/login" element={<AdminLoginPage />} />
              
              {/* Protected Routes */}
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              } />
              
              {/* Admin Routes */}
              <Route path="/admin/dashboard" element={
                <AdminRoute>
                  <AdminDashboardPage />
                </AdminRoute>
              } />
              <Route path="/admin/user/:userId" element={
                <AdminRoute>
                  <UserDashboardPage />
                </AdminRoute>
              } />
              
              {/* Default redirect */}
              <Route path="/" element={<Navigate to="/login" replace />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </Box>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App; 
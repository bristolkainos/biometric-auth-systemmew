import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

interface AdminUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_super_admin: boolean;
  is_active: boolean;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  adminUser: AdminUser | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (username: string, password: string, biometricData: { type: string; data: string }) => Promise<void>;
  adminLogin: (username: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  setTokens: (accessToken: string, refreshToken: string) => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [adminUser, setAdminUser] = useState<AdminUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing tokens on app load
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          console.log('🔍 Found existing token, checking authentication...');
          // Try to get user data first
          try {
            const userData = await authService.getCurrentUser();
            console.log('✅ Successfully authenticated as regular user:', userData.username);
            setUser(userData);
            setAdminUser(null);
          } catch (userError) {
            // If getting user data fails, try admin data
            console.log('🔄 Regular user auth failed, trying admin auth...');
            try {
              const adminData = await authService.getCurrentAdmin();
              console.log('✅ Successfully authenticated as admin user:', adminData.username);
              setAdminUser(adminData);
              setUser(null);
            } catch (adminError) {
              // If both fail, tokens are invalid - clear them
              console.log('❌ Authentication check failed for both user and admin - clearing tokens');
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              setUser(null);
              setAdminUser(null);
            }
          }
        } else {
          console.log('ℹ️ No existing token found, user needs to login');
        }
      } catch (error) {
        // Unexpected error - clear tokens
        console.log('❌ Unexpected authentication error - clearing tokens:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        setAdminUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string, biometricData: { type: string; data: string }) => {
    console.log('🔍 AuthContext.login called with:', { username, biometricType: biometricData.type });
    
    try {
      console.log('📡 Calling authService.login...');
      const response = await authService.login(username, password, biometricData);
      console.log('✅ Login response received:', response);
      
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      
      console.log('📡 Getting current user...');
      const userData = await authService.getCurrentUser();
      console.log('✅ User data received:', userData);
      
      setUser(userData);
      setAdminUser(null);
      
      console.log('✅ Login process completed successfully');
    } catch (error) {
      console.error('❌ Login error in AuthContext:', error);
      console.error('Error details:', {
        message: error instanceof Error ? error.message : 'Unknown error',
        code: (error as any)?.code,
        response: (error as any)?.response?.data,
        status: (error as any)?.response?.status
      });
      throw error;
    }
  };

  const adminLogin = async (username: string, password: string) => {
    try {
      const response = await authService.adminLogin(username, password);
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      
      const adminData = await authService.getCurrentAdmin();
      setAdminUser(adminData);
      setUser(null);
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData: any) => {
    try {
      await authService.register(userData);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setAdminUser(null);
  };

  const setTokens = async (accessToken: string, refreshToken: string) => {
    try {
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('refresh_token', refreshToken);
      
      // Determine if this is a regular user or admin by trying to get user data
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
        setAdminUser(null);
      } catch (userError) {
        // If getting user data fails, try admin data
        try {
          const adminData = await authService.getCurrentAdmin();
          setAdminUser(adminData);
          setUser(null);
        } catch (adminError) {
          // If both fail, remove tokens
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          throw new Error('Invalid tokens provided');
        }
      }
    } catch (error) {
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    adminUser,
    isAuthenticated: !!user || !!adminUser,
    isAdmin: !!adminUser,
    login,
    adminLogin,
    register,
    logout,
    setTokens,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 
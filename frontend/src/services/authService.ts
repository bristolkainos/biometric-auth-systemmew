import axios from 'axios';

export const API_BASE_URL = process.env.REACT_APP_API_URL || window.location.origin;
// Ensure API base URL includes '/api/v1' prefix for backend endpoints
const API_URL = API_BASE_URL.endsWith('/api/v1')
  ? API_BASE_URL
  : `${API_BASE_URL}/api/v1`;

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 600000, // 10 minutes timeout for biometric processing (increased from 3 minutes)
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', (config.baseURL || '') + (config.url || ''));
    console.log('Request method:', config.method);
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Token refresh state to prevent multiple simultaneous refresh requests
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: any) => void;
  reject: (error?: any) => void;
}> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  
  failedQueue = [];
};

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Don't intercept non-HTTP errors
    if (!error.response) {
      return Promise.reject(error);
    }
    
    const originalRequest = error.config;

    // Prevent infinite loops - don't retry refresh token requests
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If we're already refreshing, queue this request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await api.post('/auth/refresh', {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);

          processQueue(null, access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens
        processQueue(refreshError, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        console.log('Token refresh failed, user needs to login again');
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export interface LoginRequest {
  username: string;
  password: string;
  biometric_type: string;  // Required for user login
  biometric_data: string;  // Required for user login
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  biometric_data: Array<{
    biometric_type: string;
    image_data: string;
  }>;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface AdminResponse {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_super_admin: boolean;
  is_active: boolean;
  created_at: string;
}

class AuthService {
  async register(userData: RegisterRequest): Promise<UserResponse> {
    // Use correct backend register endpoint
    const response = await api.post('/auth/register', userData);
    return response.data;
  }

  async login(username: string, password: string, biometricData: { type: string; data: string }): Promise<TokenResponse> {
    // Use correct backend login endpoint
    console.log('Login request initiated:', { username, biometricType: biometricData.type });
    console.log('API Base URL:', API_BASE_URL);
    const loginData: LoginRequest = {
      username,
      password,
      biometric_type: biometricData.type,
      biometric_data: biometricData.data,
    };

    console.log('Login data prepared:', { ...loginData, password: '[HIDDEN]', biometric_data: '[HIDDEN]' });

    try {
      const response = await api.post('/auth/login', loginData);
      console.log('Login successful:', response.status);
      return response.data;
    } catch (error) {
      console.error('Login request failed:', error);
      throw error;
    }
  }

  async biometricLogin(biometricType: string, biometricData: Blob): Promise<TokenResponse> {
    const formData = new FormData();
    formData.append('biometric_data', biometricData, 'biometric.png');
    
    console.log('Biometric login request initiated:', { biometricType });
    
    try {
      const response = await api.post(
        `/auth/biometric-identify?modality=${biometricType}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      console.log('Biometric login successful:', response.status);
      return response.data;
    } catch (error) {
      console.error('Biometric login request failed:', error);
      throw error;
    }
  }

  // WebAuthn Methods for Mobile Fingerprint/Biometric Authentication
  async registerWebAuthnCredential(username: string, credentialData: any): Promise<any> {
    console.log('WebAuthn registration initiated:', { username });
    
    try {
      const response = await api.post('/auth/webauthn/register', {
        username,
        credential: credentialData
      });
      console.log('WebAuthn registration successful:', response.status);
      return response.data;
    } catch (error) {
      console.error('WebAuthn registration failed:', error);
      throw error;
    }
  }

  async verifyWebAuthnCredential(username: string, credentialData: any): Promise<TokenResponse> {
    console.log('WebAuthn verification initiated:', { username });
    
    try {
      const response = await api.post('/auth/webauthn/verify', {
        username,
        credential: credentialData
      });
      console.log('WebAuthn verification successful:', response.status);
      return response.data;
    } catch (error) {
      console.error('WebAuthn verification failed:', error);
      throw error;
    }
  }

  // Enhanced biometric login with WebAuthn support
  async mobileBiometricLogin(biometricType: string, credentialData: any, username?: string): Promise<TokenResponse> {
    console.log('Mobile biometric login initiated:', { biometricType });
    
    try {
      // If it's WebAuthn data, use WebAuthn verification
      if (credentialData.type === 'public-key' || credentialData.rawId) {
        if (!username) {
          throw new Error('Username required for WebAuthn authentication');
        }
        return await this.verifyWebAuthnCredential(username, credentialData);
      }
      
      // Otherwise, use traditional biometric verification
      const blob = new Blob([JSON.stringify(credentialData)], { type: 'application/json' });
      return await this.biometricLogin(biometricType, blob);
    } catch (error) {
      console.error('Mobile biometric login failed:', error);
      throw error;
    }
  }

  async adminLogin(username: string, password: string): Promise<TokenResponse> {
    const response = await api.post('/auth/admin/login', {
      username,
      password,
    });
    return response.data;
  }

  async getCurrentUser(): Promise<UserResponse> {
    const response = await api.get('/auth/me');
    return response.data;
  }

  // User Dashboard Methods with Caching
  async getUserBiometricData(): Promise<any[]> {
    const response = await api.get('/auth/me/biometrics');
    return response.data;
  }

  async getUserLoginHistory(): Promise<any[]> {
    const response = await api.get('/auth/me/login-history');
    return response.data;
  }

  async getUserSecurityOverview(): Promise<any> {
    const response = await api.get('/auth/me/security-overview');
    return response.data;
  }

  // Biometric Dashboard Methods
  async getBiometricDashboard(): Promise<any> {
    const response = await api.get('/biometric/dashboard');
    return response.data;
  }

  async getPersonalAnalytics(): Promise<any> {
    const response = await api.get('/biometric/personal-analytics');
    return response.data;
  }

  async getBiometricAnalysis(biometricId: number): Promise<any> {
    const response = await api.get(`/biometric/analysis/${biometricId}`);
    return response.data;
  }

  async getCurrentAdmin(): Promise<AdminResponse> {
    const response = await api.get('/auth/admin/me');
    return response.data;
  }

  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const response = await api.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  }

  // Generic HTTP methods for API calls
  async get(url: string, config?: any) {
    const response = await api.get(url, config);
    return response;
  }

  async post(url: string, data?: any, config?: any) {
    const response = await api.post(url, data, config);
    return response;
  }

  async put(url: string, data?: any, config?: any) {
    const response = await api.put(url, data, config);
    return response;
  }

  async delete(url: string, config?: any) {
    const response = await api.delete(url, config);
    return response;
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Admin Dashboard Methods with Caching
  async getAdminDashboard(): Promise<any> {
    const response = await api.get('/admin/dashboard');
    return response.data;
  }

  async getUsers(skip: number = 0, limit: number = 100): Promise<UserResponse[]> {
    const response = await api.get(`/admin/users?skip=${skip}&limit=${limit}`);
    return response.data;
  }

  async getUserDetails(userId: number): Promise<any> {
    const response = await api.get(`/admin/users/${userId}/details`);
    return response.data;
  }

  async getUserDashboardData(userId: number): Promise<any> {
    // Fetch specific user details for admin
    const response = await api.get(`/admin/users/${userId}`);
    // Return in expected shape for UserDashboardPage
    return {
      user: response.data,
      analytics: {},
      login_attempts: [],
      biometric_methods: []
    };
  }

  async updateUserStatus(userId: number, isActive: boolean): Promise<any> {
    const response = await api.put(`/admin/users/${userId}/status?is_active=${isActive}`);
    return response.data;
  }

  async deleteUser(userId: number): Promise<any> {
    const response = await api.delete(`/admin/users/${userId}`);
    return response.data;
  }

  async getLoginAttempts(skip: number = 0, limit: number = 100): Promise<any[]> {
    const response = await api.get(`/admin/login-attempts?skip=${skip}&limit=${limit}`);
    return response.data;
  }

  async resetUserFailedAttempts(userId: number): Promise<any> {
    const response = await api.post(`/admin/reset-user-attempts/${userId}`);
    return response.data;
  }

  async getBiometricUsageAnalytics(): Promise<any> {
    const response = await api.get('/admin/analytics/biometric-usage');
    return response.data;
  }

  async getSecurityAnalytics(): Promise<any> {
    const response = await api.get('/admin/analytics/security');
    return response.data;
  }

  async exportSystemReport(): Promise<any> {
    const response = await api.get('/admin/reports/export');
    return response.data;
  }

  // System Performance Analytics Methods
  async getModalityPerformance(): Promise<any> {
    const response = await api.get('/admin/analytics/modality-performance');
    return response.data;
  }

  async getPipelineAnalysis(): Promise<any> {
    const response = await api.get('/admin/analytics/pipeline-analysis');
    return response.data;
  }

  async getErrorAnalysis(): Promise<any> {
    const response = await api.get('/admin/analytics/error-analysis');
    return response.data;
  }

  async getSystemHealth(): Promise<any> {
    const response = await api.get('/admin/analytics/system-health');
    return response.data;
  }

  // Cache management methods
  clearUserCache(): void {
    // No caching, so no cache to clear
  }

  clearAllCache(): void {
    // No caching, so no cache to clear
  }

  refreshUserData(): void {
    // No caching, so no data to refresh
  }
}

export const authService = new AuthService();
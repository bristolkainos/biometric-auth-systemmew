import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL;

// Cache configuration
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes in milliseconds
const cache = new Map<string, { data: any; timestamp: number }>();

// Cache utility functions
const getCacheKey = (endpoint: string, params?: any) => {
  const paramString = params ? JSON.stringify(params) : '';
  return `${endpoint}${paramString}`;
};

const isCacheValid = (timestamp: number) => {
  return Date.now() - timestamp < CACHE_DURATION;
};

const getCachedData = (key: string) => {
  const cached = cache.get(key);
  if (cached && isCacheValid(cached.timestamp)) {
    console.log('Returning cached blockchain data for:', key);
    return cached.data;
  }
  return null;
};

const setCachedData = (key: string, data: any) => {
  cache.set(key, { data, timestamp: Date.now() });
  console.log('Cached blockchain data for:', key);
};

const clearCache = (pattern?: string) => {
  if (pattern) {
    // Clear specific cache entries
    Array.from(cache.keys()).forEach(key => {
      if (key.includes(pattern)) {
        cache.delete(key);
        console.log('Cleared blockchain cache for:', key);
      }
    });
  } else {
    // Clear all cache
    cache.clear();
    console.log('Cleared all blockchain cache');
  }
};

// Create axios instance for blockchain service
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout for blockchain operations
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export interface BlockchainTransaction {
  id: string;
  type: 'biometric_mint' | 'verification' | 'access_grant' | 'security_update';
  timestamp: string;
  status: 'success' | 'pending' | 'failed';
  hash: string;
  biometricType?: string;
  description: string;
  gasUsed?: number;
  blockNumber?: number;
  from: string;
  to: string;
  value?: string;
}

export interface BlockchainMetrics {
  totalTransactions: number;
  successfulTransactions: number;
  failedTransactions: number;
  averageGasUsed: number;
  lastBlockNumber: number;
  encryptionStrength: number;
  biometricTokens: number;
  securityScore: number;
  networkStatus: 'active' | 'maintenance' | 'error';
  contractAddress: string;
}

export interface BiometricToken {
  id: string;
  tokenId: string;
  biometricType: string;
  owner: string;
  mintedAt: string;
  lastVerified: string;
  verificationCount: number;
  metadata: {
    confidence: number;
    features: string[];
    imageHash: string;
  };
}

class BlockchainService {
  async getTransactionHistory(userId?: string): Promise<BlockchainTransaction[]> {
    const cacheKey = getCacheKey('/blockchain/transactions', { user_id: userId });
    const cachedData = getCachedData(cacheKey);
    
    if (cachedData) {
      return cachedData;
    }

    try {
      const response = await api.get('/blockchain/transactions', {
        params: { user_id: userId }
      });
      setCachedData(cacheKey, response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch blockchain transactions:', error);
      // Return mock data for demonstration
      const mockData = this.getMockTransactions();
      setCachedData(cacheKey, mockData);
      return mockData;
    }
  }

  async getBlockchainMetrics(): Promise<BlockchainMetrics> {
    const cacheKey = getCacheKey('/blockchain/metrics');
    const cachedData = getCachedData(cacheKey);
    
    if (cachedData) {
      return cachedData;
    }

    try {
      const response = await api.get('/blockchain/metrics');
      setCachedData(cacheKey, response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch blockchain metrics:', error);
      // Return mock data for demonstration
      const mockData = this.getMockMetrics();
      setCachedData(cacheKey, mockData);
      return mockData;
    }
  }

  async getBiometricTokens(userId?: string): Promise<BiometricToken[]> {
    const cacheKey = getCacheKey('/blockchain/biometric-tokens', { user_id: userId });
    const cachedData = getCachedData(cacheKey);
    
    if (cachedData) {
      return cachedData;
    }

    try {
      const response = await api.get('/blockchain/biometric-tokens', {
        params: { user_id: userId }
      });
      setCachedData(cacheKey, response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch biometric tokens:', error);
      // Return mock data for demonstration
      const mockData = this.getMockBiometricTokens();
      setCachedData(cacheKey, mockData);
      return mockData;
    }
  }

  async mintBiometricToken(biometricData: any): Promise<{ success: boolean; transactionHash?: string; error?: string }> {
    try {
      const response = await api.post('/blockchain/mint-token', biometricData);
      return response.data;
    } catch (error) {
      console.error('Failed to mint biometric token:', error);
      return { success: false, error: 'Failed to mint token' };
    }
  }

  async verifyBiometricToken(tokenId: string, biometricData: any): Promise<{ success: boolean; verified: boolean; confidence: number }> {
    try {
      const response = await api.post('/blockchain/verify-token', {
        tokenId,
        biometricData
      });
      return response.data;
    } catch (error) {
      console.error('Failed to verify biometric token:', error);
      return { success: false, verified: false, confidence: 0 };
    }
  }

  // Mock data methods for demonstration
  private getMockTransactions(): BlockchainTransaction[] {
    return [
      {
        id: 'tx_001',
        type: 'biometric_mint',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        biometricType: 'fingerprint',
        description: 'Fingerprint biometric token minted',
        gasUsed: 21000,
        blockNumber: 12345678,
        from: '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        to: '0x1234567890123456789012345678901234567890'
      },
      {
        id: 'tx_002',
        type: 'biometric_mint',
        timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        biometricType: 'face',
        description: 'Face recognition biometric token minted',
        gasUsed: 25000,
        blockNumber: 12345675,
        from: '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        to: '0x1234567890123456789012345678901234567890'
      },
      {
        id: 'tx_003',
        type: 'verification',
        timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        status: 'success',
        hash: '0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba',
        biometricType: 'fingerprint',
        description: 'Biometric verification completed',
        gasUsed: 15000,
        blockNumber: 12345680,
        from: '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        to: '0x1234567890123456789012345678901234567890'
      }
    ];
  }

  private getMockMetrics(): BlockchainMetrics {
    return {
      totalTransactions: 156,
      successfulTransactions: 152,
      failedTransactions: 4,
      averageGasUsed: 22000,
      lastBlockNumber: 12345682,
      encryptionStrength: 95,
      biometricTokens: 3,
      securityScore: 92,
      networkStatus: 'active',
      contractAddress: '0x1234567890123456789012345678901234567890'
    };
  }

  private getMockBiometricTokens(): BiometricToken[] {
    return [
      {
        id: '1',
        tokenId: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        biometricType: 'fingerprint',
        owner: '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        mintedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        lastVerified: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        verificationCount: 15,
        metadata: {
          confidence: 0.95,
          features: ['minutiae_points', 'ridge_patterns', 'core_points'],
          imageHash: '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890'
        }
      },
      {
        id: '2',
        tokenId: '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        biometricType: 'face',
        owner: '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
        mintedAt: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
        lastVerified: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        verificationCount: 8,
        metadata: {
          confidence: 0.92,
          features: ['facial_landmarks', 'feature_points', 'face_encoding'],
          imageHash: '0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba'
        }
      }
    ];
  }

  // Cache management methods
  clearBlockchainCache(): void {
    clearCache('/blockchain');
  }

  clearAllCache(): void {
    clearCache();
  }

  refreshBlockchainData(): void {
    this.clearBlockchainCache();
  }
}

export const blockchainService = new BlockchainService();
export default blockchainService;
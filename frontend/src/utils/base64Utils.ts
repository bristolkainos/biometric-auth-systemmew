// Utility functions for handling base64 biometric data

export const cleanBase64Data = (data: string): string => {
  try {
    // Remove data URL prefixes
    if (data.startsWith('data:')) {
      const parts = data.split(',');
      if (parts.length >= 2) {
        return parts[1];
      }
    }
    
    // Handle base64 URLs
    if (data.includes('base64,')) {
      const parts = data.split('base64,');
      if (parts.length >= 2) {
        return parts[1];
      }
    }
    
    // Remove any whitespace and line breaks
    return data.replace(/\s+/g, '');
  } catch (error) {
    console.error('Error cleaning base64 data:', error);
    throw new Error('Invalid base64 data format');
  }
};

export const validateBase64 = (data: string): boolean => {
  try {
    const cleaned = cleanBase64Data(data);
    
    // Check if it's valid base64
    const decoded = atob(cleaned);
    const reencoded = btoa(decoded);
    
    // Base64 should be reversible
    return reencoded === cleaned;
  } catch (error) {
    return false;
  }
};

export const ensureValidBase64 = (data: any): string => {
  try {
    let base64String: string;
    
    if (typeof data === 'string') {
      base64String = cleanBase64Data(data);
    } else if (typeof data === 'object') {
      // Convert object to JSON and then to base64
      base64String = btoa(JSON.stringify(data));
    } else {
      // Convert other types to string then base64
      base64String = btoa(String(data));
    }
    
    // Validate the result
    if (!validateBase64(base64String)) {
      throw new Error('Generated data is not valid base64');
    }
    
    return base64String;
  } catch (error) {
    console.error('Error ensuring valid base64:', error);
    throw new Error('Failed to create valid base64 data');
  }
};

export const getBase64Info = (data: string): {
  isValid: boolean;
  originalLength: number;
  cleanedLength: number;
  decodedSize: number;
  format: string;
} => {
  try {
    const cleaned = cleanBase64Data(data);
    const isValid = validateBase64(cleaned);
    const decoded = isValid ? atob(cleaned) : '';
    
    let format = 'unknown';
    if (data.startsWith('data:image/')) {
      format = 'image';
    } else if (data.startsWith('data:application/json')) {
      format = 'json';
    } else if (data.includes('base64,')) {
      format = 'data-url';
    } else {
      format = 'raw-base64';
    }
    
    return {
      isValid,
      originalLength: data.length,
      cleanedLength: cleaned.length,
      decodedSize: decoded.length,
      format
    };
  } catch (error) {
    return {
      isValid: false,
      originalLength: data.length,
      cleanedLength: 0,
      decodedSize: 0,
      format: 'invalid'
    };
  }
};

export const debugBase64 = (data: string, label?: string): void => {
  const info = getBase64Info(data);
  console.log(`Base64 Debug${label ? ` (${label})` : ''}:`, {
    ...info,
    preview: data.substring(0, 100) + (data.length > 100 ? '...' : '')
  });
}; 
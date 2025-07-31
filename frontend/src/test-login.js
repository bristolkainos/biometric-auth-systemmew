import axios from 'axios';

// Test direct axios call from browser console
const testLogin = async () => {
  try {
    console.log('Testing login with axios...');
    
    const response = await axios.post('https://biometric-auth-system.uc.r.appspot.com/api/v1/auth/login-fast', {
      username: 'blaq23',
      password: 'w14q4q4SAMO@#',
      biometric_type: 'face',
      biometric_data: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77gwAAAABJRU5ErkJggg=='
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });
    
    console.log('Login successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('Login failed:', error);
    if (error.response) {
      console.error('Error response:', error.response.data);
      console.error('Status:', error.response.status);
    }
    if (error.code === 'ERR_NETWORK') {
      console.error('Network error - check if backend is running');
    }
    throw error;
  }
};

// Test function for browser console
window.testLogin = testLogin;
console.log('testLogin function available. Call testLogin() to test login.');

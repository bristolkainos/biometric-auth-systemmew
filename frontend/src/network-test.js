// Simple test to isolate the network issue
// Add this to your browser console on http://localhost:3000

const testNetworkConnection = async () => {
  console.log('Testing network connection...');
  
  // Test 1: Simple fetch to backend
  try {
    const response = await fetch('https://biometric-auth-system.uc.r.appspot.com/docs');
    console.log('✅ Backend is reachable via fetch:', response.status);
  } catch (error) {
    console.error('❌ Backend fetch failed:', error);
  }
  
  // Test 2: Test CORS with login endpoint
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login-fast', {
      method: 'OPTIONS',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
      }
    });
    console.log('✅ CORS preflight successful:', response.status);
  } catch (error) {
    console.error('❌ CORS preflight failed:', error);
  }
  
  // Test 3: Test actual login request
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login-fast', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: 'blaq23',
        password: 'w14q4q4SAMO@#',
        biometric_type: 'face',
        biometric_data: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77gwAAAABJRU5ErkJggg=='
      })
    });
    
    const data = await response.json();
    console.log('✅ Login request completed:', response.status, data);
  } catch (error) {
    console.error('❌ Login request failed:', error);
  }
};

// Make function available globally
window.testNetworkConnection = testNetworkConnection;
console.log('Network test function available. Run: testNetworkConnection()');

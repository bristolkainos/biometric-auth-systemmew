"""
Comprehensive Live Test Suite for Biometric Authentication System
Tests all major functionality including registration, login, admin operations, and biometric management
"""
import requests
import json
import base64
import io
from PIL import Image
import numpy as np
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

class BiometricAuthTester:
    def __init__(self):
        self.admin_token = None
        self.user_token = None
        self.test_user_id = None
        
    def print_test(self, test_name, status="RUNNING"):
        """Print test status"""
        status_emoji = {"RUNNING": "🔄", "PASS": "✅", "FAIL": "❌", "INFO": "ℹ️"}
        print(f"{status_emoji.get(status, '🔄')} {test_name}")
    
    def create_dummy_image(self, width=200, height=200):
        """Create a dummy image for testing biometric endpoints"""
        # Create a simple test image
        img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return img_base64
    
    def test_health_check(self):
        """Test system health endpoint"""
        self.print_test("Health Check", "RUNNING")
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                assert data["status"] == "healthy"
                self.print_test("Health Check - System is healthy", "PASS")
                return True
            else:
                self.print_test(f"Health Check - Failed with status {response.status_code}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Health Check - Error: {str(e)}", "FAIL")
            return False
    
    def test_admin_login(self):
        """Test admin authentication"""
        self.print_test("Admin Login", "RUNNING")
        try:
            login_data = {
                "username": "admin",
                "password": "admin123!"
            }
            response = requests.post(f"{API_BASE}/auth/admin/login", json=login_data, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data["access_token"]
                self.print_test("Admin Login - Successfully authenticated", "PASS")
                return True
            else:
                self.print_test(f"Admin Login - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Admin Login - Error: {str(e)}", "FAIL")
            return False
    
    def test_admin_dashboard(self):
        """Test admin dashboard"""
        self.print_test("Admin Dashboard", "RUNNING")
        if not self.admin_token:
            self.print_test("Admin Dashboard - No admin token available", "FAIL")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_BASE}/admin/dashboard", headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("statistics", {})
                self.print_test(f"Admin Dashboard - Total Users: {stats.get('total_users', 0)}, " +
                              f"Active Users: {stats.get('active_users', 0)}", "INFO")
                self.print_test("Admin Dashboard - Successfully retrieved", "PASS")
                return True
            else:
                self.print_test(f"Admin Dashboard - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Admin Dashboard - Error: {str(e)}", "FAIL")
            return False
    
    def test_user_registration(self):
        """Test user registration with biometric data"""
        self.print_test("User Registration", "RUNNING")
        try:
            # Create dummy biometric data
            face_image = self.create_dummy_image()
            fingerprint_image = self.create_dummy_image()
            
            registration_data = {
                "username": f"testuser_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
                "biometric_data": [
                    {
                        "biometric_type": "face",
                        "image_data": face_image
                    },
                    {
                        "biometric_type": "fingerprint", 
                        "image_data": fingerprint_image
                    }
                ]
            }
            
            response = requests.post(f"{API_BASE}/auth/register", json=registration_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.test_user_id = data["id"]
                self.print_test(f"User Registration - Created user ID: {self.test_user_id}", "PASS")
                return True
            else:
                self.print_test(f"User Registration - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"User Registration - Error: {str(e)}", "FAIL")
            return False
    
    def test_user_login(self):
        """Test user login"""
        self.print_test("User Login", "RUNNING")
        if not self.test_user_id:
            self.print_test("User Login - No test user available", "FAIL")
            return False
            
        try:
            # Get user details first to get username
            if not self.admin_token:
                self.print_test("User Login - No admin token for user lookup", "FAIL")
                return False
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_BASE}/admin/users/{self.test_user_id}", headers=headers, timeout=5)
            
            if response.status_code != 200:
                self.print_test("User Login - Could not retrieve user details", "FAIL")
                return False
                
            user_data = response.json()
            username = user_data["username"]
            
            # Try to login
            login_data = {
                "username": username,
                "password": "TestPassword123!"
            }
            
            response = requests.post(f"{API_BASE}/auth/login", json=login_data, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.user_token = data["access_token"]
                self.print_test("User Login - Successfully authenticated", "PASS")
                return True
            else:
                self.print_test(f"User Login - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"User Login - Error: {str(e)}", "FAIL")
            return False
    
    def test_biometric_methods(self):
        """Test biometric methods endpoint"""
        self.print_test("Biometric Methods", "RUNNING")
        try:
            response = requests.get(f"{API_BASE}/biometric/methods", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                methods = data.get("available_methods", [])
                self.print_test(f"Biometric Methods - Found {len(methods)} methods", "INFO")
                for method in methods:
                    self.print_test(f"  - {method['name']} ({method['type']})", "INFO")
                self.print_test("Biometric Methods - Successfully retrieved", "PASS")
                return True
            else:
                self.print_test(f"Biometric Methods - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Biometric Methods - Error: {str(e)}", "FAIL")
            return False
    
    def test_biometric_verification(self):
        """Test biometric verification"""
        self.print_test("Biometric Verification", "RUNNING")
        if not self.user_token:
            self.print_test("Biometric Verification - No user token available", "FAIL")
            return False
            
        try:
            # Create a dummy face image for verification
            face_image = self.create_dummy_image()
            
            verification_data = {
                "biometric_type": "face",
                "image_data": face_image
            }
            
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.post(f"{API_BASE}/biometric/verify", 
                                   json=verification_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.print_test(f"Biometric Verification - Verified: {data.get('verified', False)}", "PASS")
                return True
            else:
                self.print_test(f"Biometric Verification - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Biometric Verification - Error: {str(e)}", "FAIL")
            return False
    
    def test_user_profile(self):
        """Test user profile endpoint"""
        self.print_test("User Profile", "RUNNING")
        if not self.user_token:
            self.print_test("User Profile - No user token available", "FAIL")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_BASE}/users/me", headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.print_test(f"User Profile - Username: {data.get('username')}, " +
                              f"Email: {data.get('email')}", "INFO")
                self.print_test("User Profile - Successfully retrieved", "PASS")
                return True
            else:
                self.print_test(f"User Profile - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"User Profile - Error: {str(e)}", "FAIL")
            return False
    
    def test_biometric_data_listing(self):
        """Test user's biometric data listing"""
        self.print_test("Biometric Data Listing", "RUNNING")
        if not self.user_token:
            self.print_test("Biometric Data Listing - No user token available", "FAIL")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{API_BASE}/users/biometric-data", headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                methods = data.get("biometric_methods", [])
                self.print_test(f"Biometric Data Listing - User has {len(methods)} biometric methods enrolled", "INFO")
                self.print_test("Biometric Data Listing - Successfully retrieved", "PASS")
                return True
            else:
                self.print_test(f"Biometric Data Listing - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Biometric Data Listing - Error: {str(e)}", "FAIL")
            return False
    
    def test_admin_user_management(self):
        """Test admin user management"""
        self.print_test("Admin User Management", "RUNNING")
        if not self.admin_token:
            self.print_test("Admin User Management - No admin token available", "FAIL")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_BASE}/admin/users", headers=headers, timeout=5)
            
            if response.status_code == 200:
                users = response.json()
                self.print_test(f"Admin User Management - Found {len(users)} users in system", "INFO")
                self.print_test("Admin User Management - Successfully retrieved user list", "PASS")
                return True
            else:
                self.print_test(f"Admin User Management - Failed: {response.text}", "FAIL")
                return False
        except Exception as e:
            self.print_test(f"Admin User Management - Error: {str(e)}", "FAIL")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive Live Test Suite")
        print("=" * 60)
        
        test_results = []
        
        # System tests
        test_results.append(self.test_health_check())
        
        # Admin tests
        test_results.append(self.test_admin_login())
        test_results.append(self.test_admin_dashboard())
        
        # User registration and authentication
        test_results.append(self.test_user_registration())
        test_results.append(self.test_user_login())
        
        # Biometric functionality
        test_results.append(self.test_biometric_methods())
        test_results.append(self.test_biometric_verification())
        
        # User management
        test_results.append(self.test_user_profile())
        test_results.append(self.test_biometric_data_listing())
        
        # Admin management
        test_results.append(self.test_admin_user_management())
        
        # Summary
        print("\n" + "=" * 60)
        passed = sum(test_results)
        total = len(test_results)
        
        if passed == total:
            print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
            print("✅ System is fully functional and ready for use!")
        else:
            print(f"⚠️  {passed}/{total} tests passed")
            print("❌ Some functionality may not be working correctly")
        
        return passed == total

def main():
    """Main test function"""
    print("🧪 Biometric Authentication System - Live Test Suite")
    print("Testing all major functionality...")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly. Please ensure the FastAPI server is running.")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please ensure the FastAPI server is running on http://localhost:8000")
        return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    # Run tests
    tester = BiometricAuthTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 System is ready for production use!")
    else:
        print("\n🔧 Please check the failed tests and fix any issues.")

if __name__ == "__main__":
    main()

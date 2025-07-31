#!/usr/bin/env python3
"""
Debug script to test admin authentication and plot generation
"""
import requests
import json

def debug_admin_access():
    """Debug admin authentication and API access"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🔍 Debug: Testing Admin Dashboard API Access\n")
    
    # Step 1: Test if API is accessible
    print("1. Testing API health...")
    try:
        health_response = requests.get(f"{base_url}/../", timeout=5)
        print(f"   ✅ API accessible: {health_response.status_code}")
    except Exception as e:
        print(f"   ❌ API not accessible: {e}")
        return
    
    # Step 2: Test admin login
    print("\n2. Testing admin login...")
    login_data = {
        "username": "admin@biometric-auth.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/admin/login", data=login_data, timeout=10)
        print(f"   Login response: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"   ✅ Login successful! Token: {access_token[:20]}...")
            
            # Step 3: Test plot endpoints
            print("\n3. Testing plot endpoints...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test a few key endpoints
            test_endpoints = [
                "/admin/analytics/feature-distribution-time/plot",
                "/admin/analytics/model-performance-by-class/plot",
                "/admin/analytics/modality-performance/plot"
            ]
            
            for endpoint in test_endpoints:
                try:
                    print(f"   Testing: {endpoint}")
                    plot_response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=30)
                    
                    if plot_response.status_code == 200:
                        content_type = plot_response.headers.get('content-type', 'unknown')
                        content_length = len(plot_response.content)
                        print(f"      ✅ Success: {content_type}, {content_length} bytes")
                    else:
                        error_text = plot_response.text[:200] if plot_response.text else "No error message"
                        print(f"      ❌ Failed: {plot_response.status_code} - {error_text}")
                        
                except Exception as e:
                    print(f"      ❌ Exception: {e}")
            
        else:
            error_text = login_response.text[:200] if login_response.text else "No error message"
            print(f"   ❌ Login failed: {login_response.status_code} - {error_text}")
    
    except Exception as e:
        print(f"   ❌ Login exception: {e}")
    
    # Step 4: Check frontend API configuration
    print("\n4. Checking if frontend can reach backend...")
    try:
        # This simulates what the frontend does
        frontend_test = requests.get("http://localhost:8000/api/v1/admin/analytics/feature-distribution-time/plot", 
                                   headers={"Authorization": "Bearer test"}, timeout=5)
        print(f"   Frontend simulation: {frontend_test.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend can't reach backend: {e}")

if __name__ == "__main__":
    debug_admin_access()

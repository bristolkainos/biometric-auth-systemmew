#!/usr/bin/env python3
"""
GCP Deployment Monitor
Monitors the deployment status and provides useful information
"""

import subprocess
import json
import time
from datetime import datetime

def run_gcloud_command(command):
    """Run a gcloud command and return the output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def check_deployment_status():
    """Check the current deployment status"""
    print("🚀 GCP Deployment Status Monitor")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check project configuration
    stdout, stderr, code = run_gcloud_command("gcloud config get-value project")
    if code == 0:
        print(f"📋 Project: {stdout}")
    
    # Check current deployments
    print("\n📦 Current App Engine Services:")
    stdout, stderr, code = run_gcloud_command("gcloud app services list")
    if code == 0:
        print(stdout)
    
    # Check versions
    print("\n🔄 Recent Versions:")
    stdout, stderr, code = run_gcloud_command("gcloud app versions list --limit=5")
    if code == 0:
        print(stdout)
    
    # Get app URL
    stdout, stderr, code = run_gcloud_command("gcloud app browse --no-launch-browser")
    if code == 0:
        app_url = stdout.replace("Opening ", "").replace(" in a new tab in your default browser.", "")
        print(f"\n🌐 App URL: {app_url}")
        return app_url
    
    return None

def test_deployment(app_url):
    """Test the deployed application"""
    if not app_url:
        return
        
    print(f"\n🧪 Testing Deployment at {app_url}")
    
    import requests
    try:
        # Test health endpoint
        health_response = requests.get(f"{app_url}/health", timeout=30)
        if health_response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"⚠️ Health check: Status {health_response.status_code}")
            
        # Test API docs
        docs_response = requests.get(f"{app_url}/docs", timeout=30)
        if docs_response.status_code == 200:
            print("✅ API docs: ACCESSIBLE")
        else:
            print(f"⚠️ API docs: Status {docs_response.status_code}")
            
        # Test API endpoint
        api_response = requests.get(f"{app_url}/api/v1/auth/me", timeout=30)
        if api_response.status_code == 401:  # Expected for unauthenticated request
            print("✅ API endpoint: WORKING (authentication required)")
        else:
            print(f"⚠️ API endpoint: Status {api_response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def main():
    """Main monitoring function"""
    app_url = check_deployment_status()
    
    if app_url:
        print("\n" + "=" * 50)
        print("🎉 Deployment Information:")
        print(f"🌐 Frontend URL: {app_url}")
        print(f"⚡ Backend API: {app_url}/api/v1") 
        print(f"📚 API Documentation: {app_url}/docs")
        print(f"❤️ Health Check: {app_url}/health")
        
        # Test the deployment
        test_deployment(app_url)
        
        print("\n" + "=" * 50)
        print("✨ Your biometric authentication system is deployed on GCP!")
        print("🚀 Ready for production testing!")

if __name__ == "__main__":
    main()

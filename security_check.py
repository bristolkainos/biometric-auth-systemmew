#!/usr/bin/env python3
"""
Security validation script for biometric authentication system
Checks for common security issues and misconfigurations
"""
import os
import sys
from pathlib import Path
import re

def check_hardcoded_secrets():
    """Check for hardcoded passwords, keys, and tokens in code"""
    print("🔍 Checking for hardcoded secrets...")
    
    dangerous_patterns = [
        (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
        (r'secret_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret key'),
        (r'jwt_secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded JWT secret'),
        (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
        (r'postgresql://[^:]+:[^@]+@', 'Database URL with credentials'),
        (r'mysql://[^:]+:[^@]+@', 'Database URL with credentials'),
    ]
    
    issues = []
    
    for py_file in Path('.').rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern, description in dangerous_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues.append(f"{py_file}: {description}")
        except Exception as e:
            print(f"⚠️  Could not read {py_file}: {e}")
    
    if issues:
        print("❌ Security issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ No hardcoded secrets found")
        return True

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        'SECRET_KEY',
        'JWT_SECRET', 
        'DATABASE_URL'
    ]
    
    missing_vars = []
    weak_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif value in ['your-secret-key-here-change-in-production', 
                       'your-jwt-secret-here-change-in-production']:
            weak_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
    
    if weak_vars:
        print(f"⚠️  Weak default values for: {', '.join(weak_vars)}")
    
    if not missing_vars and not weak_vars:
        print("✅ Environment variables properly configured")
        return True
    
    return False

def check_file_permissions():
    """Check for sensitive files with overly permissive permissions"""
    print("\n🔍 Checking file permissions...")
    
    sensitive_files = ['.env', '.env.local', '.env.production', 'config.py']
    issues = []
    
    for filename in sensitive_files:
        if os.path.exists(filename):
            stat = os.stat(filename)
            # Check if file is readable by others (Unix systems)
            if hasattr(stat, 'st_mode') and stat.st_mode & 0o044:
                issues.append(f"{filename} is readable by others")
    
    if issues:
        print("⚠️  File permission issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ File permissions look secure")
        return True

def check_debug_settings():
    """Check if debug mode is disabled in production"""
    print("\n🔍 Checking debug settings...")
    
    env = os.getenv('ENVIRONMENT', 'development')
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    if env == 'production' and debug:
        print("❌ Debug mode is enabled in production environment")
        return False
    else:
        print("✅ Debug settings are appropriate")
        return True

def check_cors_configuration():
    """Check CORS configuration for security issues"""
    print("\n🔍 Checking CORS configuration...")
    
    cors_origins = os.getenv('CORS_ORIGINS', '')
    
    if '*' in cors_origins:
        print("⚠️  CORS allows all origins (*) - consider restricting for production")
        return False
    else:
        print("✅ CORS origins are properly restricted")
        return True

def main():
    """Run all security checks"""
    print("🔐 Biometric Authentication System - Security Check")
    print("=" * 50)
    
    checks = [
        check_hardcoded_secrets,
        check_environment_variables,
        check_file_permissions,
        check_debug_settings,
        check_cors_configuration
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Security Check Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All security checks passed!")
        return 0
    else:
        print("⚠️  Some security issues need attention")
        return 1

if __name__ == "__main__":
    exit(main())

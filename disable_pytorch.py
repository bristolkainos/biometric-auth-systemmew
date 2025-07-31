#!/usr/bin/env python3
"""
Script to completely disable PyTorch in auth.py for cloud deployment
"""

import re

def disable_pytorch_in_auth():
    auth_file_path = "backend/app/api/v1/endpoints/auth.py"
    
    with open(auth_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all PyTorch import lines
    content = re.sub(
        r'from app\.services\.pytorch_biometric_service import get_pytorch_biometric_service',
        'from app.services.biometric_service import get_biometric_service as get_basic_service  # PyTorch disabled',
        content
    )
    
    # Replace all pytorch_service calls
    content = re.sub(
        r'pytorch_service = get_pytorch_biometric_service\(\)',
        'basic_service = get_basic_service()  # Using basic service instead of PyTorch',
        content
    )
    
    # Replace pytorch_service method calls with basic service equivalents
    content = re.sub(
        r'pytorch_service\.process_biometric_registration\(',
        'basic_service.process_face(',  # Use face processing as default
        content
    )
    
    content = re.sub(
        r'pytorch_service\.process_biometric_login\(',
        'basic_service.process_face(',  # Use face processing as default
        content
    )
    
    content = re.sub(
        r'pytorch_service\.verify_biometric\(',
        'basic_service.verify_biometric("face",',  # Add biometric type parameter
        content
    )
    
    print("Modified content to disable PyTorch")
    
    # Write back to file
    with open(auth_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Successfully disabled PyTorch in auth.py")

if __name__ == "__main__":
    disable_pytorch_in_auth()

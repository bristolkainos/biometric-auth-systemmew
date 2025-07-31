#!/usr/bin/env python3
"""
Simple Face Recognition Test
Tests if the face recognition improvements work correctly.
"""

import requests
import json
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Generate a simple test fingerprint image 
def create_test_fingerprint():
    """Create a simple test fingerprint image"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw simple ridge patterns
    for i in range(5, 290, 10):
        # Curved lines to simulate fingerprint ridges
        for j in range(0, 300, 20):
            x1, y1 = i, j
            x2, y2 = i + 150, j + 15
            draw.arc([x1, y1, x2, y2], 0, 180, fill='black', width=2)
    
    return img
def create_test_face(variation=0):
    """Create a simple test face image with optional variations"""
    img = Image.new('RGB', (300, 400), color='beige')
    draw = ImageDraw.Draw(img)
    
    # Face outline (oval)
    face_coords = [50, 50, 250, 350]
    if variation == 1:  # Slightly different angle
        face_coords = [45, 55, 245, 355]
    elif variation == 2:  # Different lighting (darker)
        img = Image.new('RGB', (300, 400), color='wheat')
        draw = ImageDraw.Draw(img)
    
    draw.ellipse(face_coords, fill='peachpuff', outline='black', width=2)
    
    # Eyes
    eye_y = 120 + (5 if variation == 1 else 0)
    draw.ellipse([80, eye_y, 110, eye_y + 20], fill='white', outline='black')
    draw.ellipse([90, eye_y + 5, 100, eye_y + 15], fill='black')
    
    draw.ellipse([190, eye_y, 220, eye_y + 20], fill='white', outline='black')
    draw.ellipse([200, eye_y + 5, 210, eye_y + 15], fill='black')
    
    # Nose
    nose_y = 160 + (3 if variation == 1 else 0)
    draw.line([(150, nose_y), (150, nose_y + 40)], fill='black', width=2)
    draw.arc([145, nose_y + 35, 155, nose_y + 45], 0, 180, fill='black')
    
    # Mouth
    mouth_y = 220 + (3 if variation == 1 else 0)
    draw.arc([130, mouth_y, 170, mouth_y + 20], 0, 180, fill='red', width=3)
    
    return img

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def test_face_recognition():
    """Test face recognition with realistic variations"""
    print("🔬 Simple Face Recognition Test")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Create test faces
    print("📷 Creating test biometric images...")
    base_face = create_test_face(0)  # Original
    similar_face = create_test_face(1)  # Slight variation (same person)
    different_face = create_test_face(2)  # Different lighting (same person)
    fingerprint = create_test_fingerprint()  # Fingerprint for 2-factor requirement
    
    print("✅ Test biometric images created")
    
    # Register user with base face AND fingerprint (system requires 2 biometrics)
    print("\n🔐 Registering user with face and fingerprint...")
    import time
    timestamp = int(time.time())
    register_data = {
        "username": f"face_test_user_{timestamp}",
        "password": "TestPass123!",
        "email": f"facetest{timestamp}@example.com",
        "first_name": "Face",
        "last_name": "Test",
        "biometric_data": [
            {
                "biometric_type": "face",
                "image_data": image_to_base64(base_face)
            },
            {
                "biometric_type": "fingerprint", 
                "image_data": image_to_base64(fingerprint)
            }
        ]
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/register", json=register_data)
        print(f"Registration response: {response.status_code}")
        if response.status_code != 200:
            print(f"Registration failed: {response.text}")
            return
        print("✅ User registered successfully")
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 1: Login with similar face (should succeed with relaxed thresholds)
    print("\n🔍 Test 1: Login with similar face (slight variation)...")
    login_data = {
        "username": f"face_test_user_{timestamp}",
        "password": "TestPass123!",
        "biometric_type": "face",
        "biometric_data": image_to_base64(similar_face)
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Test 1 PASSED: Similar face accepted (good!)")
        else:
            print(f"⚠️  Test 1 FAILED: Similar face rejected: {response.text}")
    except Exception as e:
        print(f"❌ Test 1 error: {e}")
    
    # Test 2: Login with different lighting (should succeed with relaxed thresholds)
    print("\n🔍 Test 2: Login with different lighting...")
    login_data2 = {
        "username": f"face_test_user_{timestamp}",
        "password": "TestPass123!",
        "biometric_type": "face",
        "biometric_data": image_to_base64(different_face)
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data2)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Test 2 PASSED: Different lighting accepted (good!)")
        else:
            print(f"⚠️  Test 2 FAILED: Different lighting rejected: {response.text}")
    except Exception as e:
        print(f"❌ Test 2 error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Face recognition test completed!")
    print("💡 If tests failed, the thresholds might need further adjustment.")

if __name__ == "__main__":
    test_face_recognition()

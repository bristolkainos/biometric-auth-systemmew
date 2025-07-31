from jose import jwt
from datetime import datetime, timedelta

# Use the same secret as the backend
JWT_SECRET = "your-jwt-secret-here-change-in-production"
JWT_ALGORITHM = "HS256"


def test_token():
    print("Testing JWT token generation and validation...")
    
    # Create a test token
    payload = {
        "sub": 4,  # User ID from logs
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    
    # Generate token
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(f"Generated token: {token[:50]}...")
    
    # Decode token
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f"✅ Token decoded successfully: {decoded}")
        return True
    except Exception as e:
        print(f"❌ Token decode failed: {e}")
        return False


if __name__ == "__main__":
    test_token() 
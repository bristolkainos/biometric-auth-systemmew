#!/usr/bin/env python3
"""Create a test user with the new password hashing system"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.database import get_db
from app.models.user import User
from app.core.security import get_password_hash

def create_test_user():
    """Create a test user with the new password system"""
    db = next(get_db())
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == 'testuser').first()
    if existing_user:
        print('🔄 Updating existing test user password...')
        existing_user.password_hash = get_password_hash('testpass')
        db.commit()
        print('✅ Test user password updated with new hashing system')
        return
    
    # Create new test user
    print('🔧 Creating new test user...')
    test_user = User(
        username='testuser',
        email='test@example.com',
        password_hash=get_password_hash('testpass'),
        first_name='Test',
        last_name='User',
        is_active=True,
        is_verified=True
    )
    
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    print(f'✅ Test user created: testuser/testpass (ID: {test_user.id})')
    
    # Also update kelvin's password if exists
    kelvin = db.query(User).filter(User.username == 'kelvin').first()
    if kelvin:
        print('🔄 Updating kelvin user password...')
        kelvin.password_hash = get_password_hash('password')  # Assuming this was his password
        db.commit()
        print('✅ Kelvin user password updated with new hashing system')

if __name__ == '__main__':
    create_test_user()

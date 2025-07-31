#!/usr/bin/env python3
"""
Create an admin user for the biometric authentication system
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from app.core.database import get_db
    from app.models.admin_user import AdminUser
    from app.core.security import get_password_hash
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import bcrypt
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the project root directory and have installed dependencies")
    sys.exit(1)

def create_admin_user():
    """Create an admin user"""
    try:
        # Database URL - adjust as needed
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/biometric_auth")
        
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as db:
            # Check if admin user already exists
            existing_admin = db.query(AdminUser).filter(AdminUser.email == "admin@biometric-auth.com").first()
            
            if existing_admin:
                print("✅ Admin user already exists!")
                print(f"   Email: admin@biometric-auth.com")
                print(f"   Role: {existing_admin.role}")
                return
            
            # Create new admin user
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            admin_user = AdminUser(
                email="admin@biometric-auth.com",
                username="admin",
                hashed_password=hashed_password,
                role="super_admin",
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print("🎉 Admin user created successfully!")
            print(f"   Email: admin@biometric-auth.com")
            print(f"   Password: admin123")
            print(f"   Role: super_admin")
            print(f"   ID: {admin_user.id}")
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        print("Make sure your database is running and accessible")

if __name__ == "__main__":
    create_admin_user()

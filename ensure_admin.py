#!/usr/bin/env python3
"""
Ensure admin user exists
"""
import asyncio
import sys
import os
from pathlib import Path
import bcrypt

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def create_admin_if_not_exists():
    try:
        from app.core.database import SessionLocal
        from app.models.admin_user import AdminUser
        
        db = SessionLocal()
        
        # Check if admin exists
        existing_admin = db.query(AdminUser).filter(AdminUser.email == "admin@biometric-auth.com").first()
        
        if existing_admin:
            print("✅ Admin user already exists:")
            print(f"   Email: {existing_admin.email}")
            print(f"   ID: {existing_admin.id}")
            print(f"   Role: {existing_admin.role}")
            print(f"   Active: {existing_admin.is_active}")
        else:
            print("🔧 Creating admin user...")
            
            # Hash password
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Create admin user
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
            
            print("✅ Admin user created successfully!")
            print(f"   Email: admin@biometric-auth.com")
            print(f"   Password: admin123")
            print(f"   ID: {admin_user.id}")
            print(f"   Role: {admin_user.role}")
        
        db.close()
        print("\n🚀 You can now login with:")
        print("   Email: admin@biometric-auth.com")
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_admin_if_not_exists()

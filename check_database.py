#!/usr/bin/env python3
"""
Check database connection and admin user
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from app.core.database import SessionLocal
    from app.models.admin_user import AdminUser
    from sqlalchemy import text
    
    def check_database():
        print("🔍 Checking database connection and admin user...")
        
        try:
            db = SessionLocal()
            
            # Test database connection
            result = db.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Check for admin users
            admin_users = db.query(AdminUser).all()
            print(f"📊 Found {len(admin_users)} admin users:")
            
            for user in admin_users:
                print(f"   - ID: {user.id}")
                print(f"   - Email: {user.email}")
                print(f"   - Username: {user.username}")
                print(f"   - Role: {user.role}")
                print(f"   - Active: {user.is_active}")
                print(f"   - Created: {user.created_at}")
                print()
            
            if not admin_users:
                print("❌ No admin users found! Creating one now...")
                
                import bcrypt
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
                
                print("✅ Admin user created successfully!")
                print(f"   Email: admin@biometric-auth.com")
                print(f"   Password: admin123")
            
            db.close()
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            print("\nMake sure your database is running!")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the project root and dependencies are installed")

if __name__ == "__main__":
    check_database()

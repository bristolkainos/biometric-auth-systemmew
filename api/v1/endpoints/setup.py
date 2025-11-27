"""Setup endpoints for initial configuration"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from admin_user import AdminUser
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/create-admin")
async def create_admin_user(db: Session = Depends(get_db)):
    """
    Create default admin user if it doesn't exist
    This endpoint is for initial setup only
    """
    try:
        # Check if admin exists
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if existing_admin:
            return {
                "status": "exists",
                "message": "Admin user already exists",
                "username": existing_admin.username
            }
        
        # Create admin user
        password_hash = pwd_context.hash("Admin@123")
        admin_user = AdminUser(
            username="admin",
            email="admin@biometric-auth.com",
            password_hash=password_hash,
            first_name="System",
            last_name="Administrator",
            is_super_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        logger.info(f"Admin user created successfully with ID: {admin_user.id}")
        
        return {
            "status": "created",
            "message": "Admin user created successfully",
            "username": "admin",
            "password": "Admin@123",
            "email": "admin@biometric-auth.com",
            "warning": "Please change the password after first login"
        }
        
    except Exception as e:
        logger.error(f"Error creating admin user: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating admin user: {str(e)}")

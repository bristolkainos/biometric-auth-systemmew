"""
Database initialization script
Creates default admin user and sets up initial data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
# Import all models to ensure proper initialization
from app.models.user import User
from app.models.admin_user import AdminUser
from app.models.biometric_data import BiometricData
from app.models.login_attempt import LoginAttempt
from app.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize database with tables and default data"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create default admin user if it doesn't exist
        admin_user = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not admin_user:
            admin_user = AdminUser(
                username="admin",
                email="admin@biometric-auth.com",
                password_hash=get_password_hash("admin123!"),
                first_name="System",
                last_name="Administrator",
                is_super_admin=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("Default admin user created (username: admin, password: admin123!)")
        else:
            logger.info("Admin user already exists")
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()

import sys
import os

# Add backend directory to path
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)

# Register all models so SQLAlchemy knows about relationships
import app.models.user
import app.models.admin_user
import app.models.biometric_data
import app.models.login_attempt

from app.core.database import get_db
from app.models.admin_user import AdminUser
from app.core.security import get_password_hash


def set_admin_password():
    db = next(get_db())
    admin = db.query(AdminUser).filter(AdminUser.username == 'admin').first()
    if admin:
        admin.password_hash = get_password_hash('admin')
        db.commit()
        print('✅ Admin password updated to: admin')
    else:
        # Create admin user if it doesn't exist
        admin = AdminUser(
            username='admin',
            email='admin@biometric-auth.com',
            password_hash=get_password_hash('admin'),
            is_active=True
        )
        db.add(admin)
        db.commit()
        print('✅ Admin user created with username: admin, password: admin')


if __name__ == '__main__':
    set_admin_password() 
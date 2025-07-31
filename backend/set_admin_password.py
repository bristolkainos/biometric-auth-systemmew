import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.database import get_db
from app.models.admin import AdminUser
from app.core.security import get_password_hash

def set_admin_password():
    db = next(get_db())
    admin = db.query(AdminUser).filter(AdminUser.username == 'admin').first()
    if admin:
        admin.password_hash = get_password_hash('admin')
        db.commit()
        print('✅ Admin password set to admin')
    else:
        print('❌ No admin user found')

if __name__ == '__main__':
    set_admin_password() 
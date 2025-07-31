import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from passlib.context import CryptContext
import sys
import os
from core.database import get_db
from admin_user import AdminUser
from core.security import get_password_hash

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

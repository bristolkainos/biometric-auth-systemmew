
#!/usr/bin/env python3
"""
Database connection check script
Uses environment variables for secure connection
"""
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to PostgreSQL using environment variables
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'railway'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', ''),
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '5432'))
)
cursor = conn.cursor()


print('=== TABLES IN DATABASE ===')
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
tables = cursor.fetchall()
for table in tables:
    print(f'Table: {table[0]}')


print('\n=== USERS TABLE ===')
try:
    cursor.execute('SELECT id, username, email FROM users LIMIT 10')
    users = cursor.fetchall()
    for user in users:
        print(f'ID: {user[0]}, Username: {user[1]}, Email: {user[2]}')
except Exception as e:
    print(f'Error reading users: {e}')


print('\n=== BIOMETRIC_DATA TABLE ===')
try:
    cursor.execute('SELECT id, user_id, biometric_type FROM biometric_data LIMIT 10')
    biometrics = cursor.fetchall()
    for bio in biometrics:
        print(f'ID: {bio[0]}, User ID: {bio[1]}, Type: {bio[2]}')
except Exception as e:
    print(f'Error reading biometric_data: {e}')

conn.close()

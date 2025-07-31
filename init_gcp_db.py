import psycopg2
from dotenv import load_dotenv
import os
import sys

def init_gcp_database():
    print("Initializing GCP PostgreSQL database...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Connect to GCP PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'bio_login'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'w14q4q4'),
            host=os.getenv('DB_HOST', '35.226.111.185'),
            port=os.getenv('DB_PORT', '5432')
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Enable UUID extension if not exists
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        
        # Create tables if they don't exist
        create_tables_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            is_active BOOLEAN DEFAULT true,
            is_verified BOOLEAN DEFAULT false,
            failed_login_attempts INTEGER DEFAULT 0,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Biometric data table
        CREATE TABLE IF NOT EXISTS biometric_data (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            biometric_type VARCHAR(20) NOT NULL CHECK (biometric_type IN ('fingerprint', 'face', 'palmprint')),
            biometric_hash VARCHAR(255) NOT NULL,
            biometric_features TEXT,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, biometric_type)
        );

        -- Login attempts table
        CREATE TABLE IF NOT EXISTS login_attempts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            username VARCHAR(50),
            attempt_type VARCHAR(20) NOT NULL CHECK (attempt_type IN ('password', 'fingerprint', 'face', 'palmprint')),
            success BOOLEAN NOT NULL,
            ip_address INET,
            user_agent TEXT,
            location_info JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Admin users table
        CREATE TABLE IF NOT EXISTS admin_users (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
            role VARCHAR(20) DEFAULT 'admin',
            permissions JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cur.execute(create_tables_sql)
        conn.commit()
        
        print("✅ GCP PostgreSQL database initialized successfully!")
        
        # Verify tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        print("\nVerified tables:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Close connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error initializing GCP database:")
        print(f"Error details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_gcp_database()

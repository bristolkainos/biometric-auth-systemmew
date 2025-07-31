-- Biometric Authentication System Database Schema
-- Initialize database tables and admin user

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
    biometric_features TEXT, -- JSON string for additional features
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, biometric_type)
);

-- Login attempts table for audit trail
CREATE TABLE IF NOT EXISTS login_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    username VARCHAR(50), -- Store username even if user is deleted
    attempt_type VARCHAR(20) NOT NULL CHECK (attempt_type IN ('password', 'fingerprint', 'face', 'palmprint')),
    success BOOLEAN NOT NULL,
    ip_address INET,
    user_agent TEXT,
    location_info JSONB, -- Store geolocation if available
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin users table
CREATE TABLE IF NOT EXISTS admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    is_super_admin BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin actions audit table
CREATE TABLE IF NOT EXISTS admin_actions (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER REFERENCES admin_users(id),
    action_type VARCHAR(50) NOT NULL,
    target_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    target_username VARCHAR(50),
    action_details JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System configuration table
CREATE TABLE IF NOT EXISTS system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_by INTEGER REFERENCES admin_users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_biometric_data_user_id ON biometric_data(user_id);
CREATE INDEX IF NOT EXISTS idx_biometric_data_type ON biometric_data(biometric_type);
CREATE INDEX IF NOT EXISTS idx_login_attempts_user_id ON login_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_login_attempts_created_at ON login_attempts(created_at);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);

-- Insert default admin user (password: admin123)
INSERT INTO admin_users (username, email, password_hash, first_name, last_name, is_super_admin) 
VALUES (
    'admin',
    'admin@company.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8mG', -- admin123
    'System',
    'Administrator',
    true
) ON CONFLICT (username) DO NOTHING;

-- Insert default system configurations
INSERT INTO system_config (config_key, config_value, description) VALUES
('max_login_attempts', '5', 'Maximum failed login attempts before account lockout'),
('lockout_duration_minutes', '30', 'Account lockout duration in minutes'),
('session_timeout_hours', '24', 'Session timeout in hours'),
('min_biometric_methods', '2', 'Minimum biometric methods required for registration'),
('password_min_length', '8', 'Minimum password length'),
('require_special_chars', 'true', 'Require special characters in password'),
('enable_audit_logging', 'true', 'Enable detailed audit logging'),
('allowed_file_types', 'jpg,jpeg,png,tiff,bmp', 'Allowed image file types for biometric uploads'),
('max_file_size_mb', '10', 'Maximum file size for biometric uploads in MB')
ON CONFLICT (config_key) DO NOTHING;

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_biometric_data_updated_at BEFORE UPDATE ON biometric_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_admin_users_updated_at BEFORE UPDATE ON admin_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_system_config_updated_at BEFORE UPDATE ON system_config FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); 
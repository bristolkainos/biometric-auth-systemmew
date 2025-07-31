#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

async def fix_feature_dimension_mismatch():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print("No DATABASE_URL found")
        return
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("=== Feature Dimension Mismatch Fix Options ===")
        print()
        
        # Option 1: Delete incompatible biometric data (recommended)
        print("Option 1: Clean up incompatible biometric data")
        print("This will remove biometric data with old dimensions so users can re-register")
        
        # Find records with wrong dimensions
        old_dimension_records = await conn.fetch("""
            SELECT id, user_id, biometric_type, 
                   length(biometric_features::text) as feature_length,
                   created_at 
            FROM biometric_data 
            WHERE biometric_type = 'face' 
            AND jsonb_array_length(biometric_features::jsonb) != 2048
            AND jsonb_array_length(biometric_features::jsonb) > 0
        """)
        
        print(f"Found {len(old_dimension_records)} records with incompatible dimensions:")
        for record in old_dimension_records:
            user_result = await conn.fetchrow("SELECT username FROM users WHERE id = $1", record['user_id'])
            username = user_result['username'] if user_result else 'Unknown'
            print(f"  User {record['user_id']} ({username}): Record ID {record['id']}")
        
        if old_dimension_records:
            print()
            print("Would you like to:")
            print("1. Delete these incompatible records (users will need to re-register)")
            print("2. Keep them (login will fail until manually fixed)")
            
        await conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(fix_feature_dimension_mismatch())

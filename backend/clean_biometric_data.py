#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

async def clean_incompatible_biometric_data():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print("No DATABASE_URL found")
        return
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("=== Cleaning Incompatible Biometric Data ===")
        
        # Delete records with wrong dimensions (not 2048)
        result = await conn.execute("""
            DELETE FROM biometric_data 
            WHERE biometric_type = 'face' 
            AND (
                jsonb_array_length(biometric_features::jsonb) != 2048
                OR jsonb_array_length(biometric_features::jsonb) = 0
            )
            AND biometric_features::text != '[]'
        """)
        
        # Extract number of deleted records from result
        deleted_count = int(result.split()[-1])
        print(f"Deleted {deleted_count} incompatible biometric records")
        
        # Show remaining records
        remaining = await conn.fetch("""
            SELECT id, user_id, biometric_type,
                   jsonb_array_length(biometric_features::jsonb) as feature_count
            FROM biometric_data 
            WHERE biometric_type = 'face'
            ORDER BY user_id
        """)
        
        print(f"Remaining compatible records: {len(remaining)}")
        for record in remaining:
            user_result = await conn.fetchrow("SELECT username FROM users WHERE id = $1", record['user_id'])
            username = user_result['username'] if user_result else 'Unknown'
            print(f"  User {record['user_id']} ({username}): {record['feature_count']} features")
        
        await conn.close()
        print()
        print("✅ Cleanup complete! Users with deleted biometric data can now re-register.")
        print("🔄 User 'silas' can now register new biometric data and login successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(clean_incompatible_biometric_data())

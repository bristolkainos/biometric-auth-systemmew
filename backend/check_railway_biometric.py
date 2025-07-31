#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
import asyncpg
import json

load_dotenv()

async def check_railway_biometric_data():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print("No DATABASE_URL found")
        return
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Check biometric data
        result = await conn.fetch("""
            SELECT id, user_id, biometric_type, 
                   length(biometric_features::text) as feature_length,
                   created_at 
            FROM biometric_data 
            WHERE biometric_type = 'face'
            ORDER BY created_at DESC
        """)
        
        print("=== Railway PostgreSQL Biometric Data ===")
        print(f"Found {len(result)} face biometric records:")
        
        for row in result:
            print(f"ID: {row['id']}, User: {row['user_id']}, Type: {row['biometric_type']}")
            print(f"  Feature JSON Length: {row['feature_length']} chars")
            print(f"  Created: {row['created_at']}")
            
            # Get actual feature dimensions
            features_result = await conn.fetchval("""
                SELECT biometric_features FROM biometric_data WHERE id = $1
            """, row['id'])
            
            if features_result:
                try:
                    features = json.loads(features_result)
                    print(f"  Actual Feature Dimensions: {len(features) if isinstance(features, list) else 'Not a list'}")
                except:
                    print(f"  Feature parsing error")
            print()
        
        # Check users
        users = await conn.fetch("SELECT id, username FROM users ORDER BY id")
        print(f"Users in database: {len(users)}")
        for user in users:
            print(f"  User {user['id']}: {user['username']}")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error connecting to Railway database: {e}")

if __name__ == "__main__":
    asyncio.run(check_railway_biometric_data())

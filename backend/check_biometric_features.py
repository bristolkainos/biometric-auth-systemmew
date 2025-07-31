#!/usr/bin/env python3
"""
Biometric features check script
Uses environment variables for secure database connection
"""
import psycopg2
import json
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_biometric_features():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'bio_login'),
        user=os.getenv('DB_USER', 'postgres'), 
        password=os.getenv('DB_PASSWORD', 'w14q4q4'),
        host=os.getenv('DB_HOST', '35.226.111.185'),
        port=int(os.getenv('DB_PORT', '5432'))
    )
    cursor = conn.cursor()
    
    # Check all biometric data
    cursor.execute('SELECT id, user_id, biometric_type, biometric_features, created_at FROM biometric_data WHERE biometric_type = %s', ("face",))
    results = cursor.fetchall()
    
    print("=== Biometric Data Analysis ===")
    for row in results:
        id, user_id, bio_type, features_json, created_at = row
        
        if features_json:
            try:
                features = json.loads(features_json)
                if isinstance(features, list):
                    feature_dims = len(features)
                else:
                    feature_dims = "Not a list"
                
                print(f"ID: {id}, User: {user_id}, Type: {bio_type}")
                print(f"  Feature Dimensions: {feature_dims}")
                print(f"  Created: {created_at}")
                print(f"  Sample features (first 5): {features[:5] if isinstance(features, list) and len(features) > 5 else 'N/A'}")
                print()
            except json.JSONDecodeError:
                print(f"ID: {id}, User: {user_id} - Invalid JSON in features")
        else:
            print(f"ID: {id}, User: {user_id} - No features stored")
    
    conn.close()

if __name__ == "__main__":
    check_biometric_features()

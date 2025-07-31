import json
from app.core.database import SessionLocal
from app.models.biometric_data import BiometricData
from app.models.user import User

desired_dim = 2048  # ResNet50 feature size

def get_feature_dim(features_str):
    try:
        features = json.loads(features_str)
        if isinstance(features, list):
            return len(features)
        elif isinstance(features, dict) and 'features' in features:
            return len(features['features'])
        else:
            return None
    except Exception:
        return None

def main():
    db = SessionLocal()
    invalid = db.query(BiometricData).filter(BiometricData.is_active == True).all()
    deleted = 0
    for bio in invalid:
        dim = get_feature_dim(bio.biometric_features)
        if dim != desired_dim:
            print(f"Deleting biometric id={bio.id} user_id={bio.user_id} type={bio.biometric_type} dim={dim}")
            db.delete(bio)
            deleted += 1
    db.commit()
    print(f"Deleted {deleted} invalid biometric records.")
    db.close()

if __name__ == "__main__":
    main()

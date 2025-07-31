#!/usr/bin/env python3
"""
Model Download Script for Biometric Authentication System
========================================================

This script downloads large model files that are too big for GitHub.
"""

import os
import requests
import zipfile
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(url: str, filepath: str, chunk_size: int = 8192):
    """Download a file with progress tracking"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        logger.info(f"Downloaded {downloaded}/{total_size} bytes ({progress:.1f}%)")
        
        logger.info(f"Successfully downloaded: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False

def download_models():
    """Download all required model files"""
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Model URLs (replace with actual URLs)
    models = {
        # Face recognition models
        "face_cnn.h5": "https://example.com/models/face_cnn.h5",
        "face_autoencoder.h5": "https://example.com/models/face_autoencoder.h5",
        "face_siamese_embedding.h5": "https://example.com/models/face_siamese_embedding.h5",
        
        # Fingerprint models
        "fingerprint_cnn.h5": "https://example.com/models/fingerprint_cnn.h5",
        "fingerprint_autoencoder.h5": "https://example.com/models/fingerprint_autoencoder.h5",
        "fingerprint_siamese_embedding.h5": "https://example.com/models/fingerprint_siamese_embedding.h5",
        
        # Palmprint models
        "palmprint_cnn.h5": "https://example.com/models/palmprint_cnn.h5",
        "palmprint_autoencoder.h5": "https://example.com/models/palmprint_autoencoder.h5",
        "palmprint_siamese_embedding.h5": "https://example.com/models/palmprint_siamese_embedding.h5",
    }
    
    logger.info("Starting model downloads...")
    
    for model_name, url in models.items():
        model_path = models_dir / model_name
        
        if model_path.exists():
            logger.info(f"Model already exists: {model_name}")
            continue
            
        logger.info(f"Downloading {model_name}...")
        if download_file(url, str(model_path)):
            logger.info(f"✅ Downloaded: {model_name}")
        else:
            logger.warning(f"⚠️ Failed to download: {model_name}")
    
    logger.info("Model download process completed!")

def download_from_zip(zip_url: str, extract_to: str = "models"):
    """Download and extract models from a zip file"""
    try:
        logger.info(f"Downloading models zip from: {zip_url}")
        
        # Download zip file
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()
        
        zip_path = "models.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Extract zip file
        logger.info("Extracting models...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Clean up
        os.remove(zip_path)
        logger.info("✅ Models extracted successfully!")
        
    except Exception as e:
        logger.error(f"Failed to download/extract models: {e}")

def check_models():
    """Check which models are missing"""
    models_dir = Path("models")
    required_models = [
        "face_cnn.h5",
        "fingerprint_cnn.h5", 
        "palmprint_cnn.h5"
    ]
    
    missing_models = []
    for model in required_models:
        if not (models_dir / model).exists():
            missing_models.append(model)
    
    if missing_models:
        logger.warning(f"Missing models: {missing_models}")
        return False
    else:
        logger.info("✅ All required models are present!")
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            check_models()
        elif sys.argv[1] == "download":
            download_models()
        elif sys.argv[1] == "zip":
            if len(sys.argv) > 2:
                download_from_zip(sys.argv[2])
            else:
                print("Usage: python download_models.py zip <zip_url>")
        else:
            print("Usage: python download_models.py [check|download|zip <url>]")
    else:
        # Default: check and download if needed
        if not check_models():
            print("Some models are missing. Run: python download_models.py download") 
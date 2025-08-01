#!/usr/bin/env python
# download_resnet50.py
# This script will download and cache the ResNet50 weights permanently for PyTorch/torchvision
# Run this once during deployment or build to ensure the model is always available

try:
    import torch
    from torchvision import models
    
    if __name__ == "__main__":
        print("🔄 Downloading ResNet50 weights...")
        # This will download and cache the weights in ~/.cache/torch/hub/checkpoints/
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        print("✅ ResNet50 weights downloaded and cached successfully!")
        print(f"📦 Model cached at: {torch.hub.get_dir()}")

except ImportError as e:
    print("⚠️ PyTorch not available during build phase:")
    print(f"   Error: {e}")
    print("💡 ResNet50 weights will be downloaded at runtime when PyTorch is available")
    print("✅ Build can continue without PyTorch - traditional features will be used")

except Exception as e:
    print(f"❌ Error downloading ResNet50 weights: {e}")
    print("💡 ResNet50 weights will be downloaded at runtime if PyTorch is available")
    print("✅ Build can continue - traditional features will be used as fallback")

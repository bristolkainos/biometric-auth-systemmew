# This script will download and cache the ResNet50 weights permanently for PyTorch/torchvision
# Run this once during deployment or build to ensure the model is always available

import torch
from torchvision import models

if __name__ == "__main__":
    print("Downloading ResNet50 weights...")
    # This will download and cache the weights in ~/.cache/torch/hub/checkpoints/
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    print("ResNet50 weights downloaded and cached successfully!")

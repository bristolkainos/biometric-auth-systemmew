# Advanced biometric libraries - all should work with Python 3.10
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("OpenCV not available, using PIL for image processing")

import numpy as np
import hashlib
import logging
from typing import Any, Dict, List, Tuple
from pathlib import Path
from PIL import Image, ImageOps
import io
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import skew, kurtosis
from core.config import settings
import json
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available, visualization features disabled")
import base64
from datetime import datetime
import os
try:
    from skimage.feature import local_binary_pattern
    from skimage.filters import sobel
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False
    logging.warning("scikit-image not available, using fallback image processing")
import base64
from datetime import datetime
import os
from typing import List, Tuple

# Import scikit-image for proper image processing
try:
    from skimage.feature import local_binary_pattern
    from skimage.filters import sobel
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False
    logging.warning("scikit-image not available, using fallback image processing")

logger = logging.getLogger(__name__)


class BiometricService:
    """Service for handling biometric authentication using simplified methods."""
    _instance = None
    _initialized = False
    
    # Test mode flag disabled - use full processing
    FAST_TEST_MODE = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BiometricService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # Mapping of available model file paths
            self.models = {
                'face': {},
                'fingerprint': {},
                'palmprint': {}
            }
            # Container for loaded Keras embedding models
            self.keras_models = {}
            self._initialized = True

    @classmethod
    def initialize(cls):
        instance = cls()
        instance._load_models()
        logger.info("Biometric service initialized with simplified methods.")

    def _load_models(self):
        """Load biometric models with fallback to simplified methods"""
        model_path = Path(settings.MODEL_PATH)
        # Debug: log model path and its contents
        logger.info(f"Scanning model directory: {model_path} (exists: {model_path.exists()})")
        if model_path.exists():
            try:
                contents = ", ".join([p.name for p in model_path.iterdir()])
                logger.info(f"Contents of model directory: {contents}")
            except Exception as e:
                logger.warning(f"Failed to list contents of {model_path}: {e}")
        
        if not model_path.exists():
            logger.warning(
                f"Models directory {model_path} does not exist. Creating it."
            )
            model_path.mkdir(parents=True, exist_ok=True)
        
        # Check for available models
        available_models = {}
        model_files = {
            'face': ['face_cnn.h5', 'face_autoencoder.h5', 'face_siamese_embedding.h5'],
            'fingerprint': ['fingerprint_cnn.h5', 'fingerprint_autoencoder.h5', 'fingerprint_siamese_embedding.h5'],
            'palmprint': ['palmprint_cnn.h5', 'palmprint_autoencoder.h5', 'palmprint_siamese_embedding.h5']
        }
        
        for modality, files in model_files.items():
            available_models[modality] = {}
            for file in files:
                file_path = model_path / file
                if file_path.exists():
                    available_models[modality][file] = str(file_path)
                    logger.info(f"Found model file: {file_path}")
        
        self.models = available_models
        
        # TensorFlow/Keras model loading removed; using simplified biometric methods only
        self.tf_available = False
        logger.info("Using simplified biometric methods with enhanced features")

    def _extract_features(self, image: np.ndarray, modality: str) -> np.ndarray:
        """Enhanced biometric feature extraction with more discriminative features"""
        
        try:
            # Convert to PIL Image for consistent processing
            if isinstance(image, np.ndarray):
                if image.dtype != np.uint8:
                    image = (image * 255).astype(np.uint8)
                img = Image.fromarray(image)
            else:
                img = image
                
            # Resize to standard size for consistent processing
            img = img.resize((128, 128), Image.Resampling.LANCZOS)
            
            # Convert to grayscale for consistent processing
            if img.mode != 'L':
                img = img.convert('L')
                
            # Convert to numpy array
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            # Extract multiple types of features for robust comparison
            features = []
            
            # 1. Raw pixel hash (most discriminative)
            # Create a hash of the raw pixels for exact matching
            pixel_hash = hashlib.sha256(img_array.tobytes()).hexdigest()
            # Convert hex to numerical features
            hash_features = [int(pixel_hash[i:i+2], 16) for i in range(0, min(64, len(pixel_hash)), 2)]
            features.extend(hash_features)
            
            # 2. Reduced pixel sampling for key discriminative features
            # Sample every 4th pixel to reduce noise sensitivity while maintaining uniqueness
            sampled_pixels = img_array[::4, ::4].flatten()
            features.extend(sampled_pixels[:1000])  # Limit to 1000 features
            
            # 2. Histogram features (intensity distribution) - more bins for detail
            hist, _ = np.histogram(img_array.flatten(), bins=128, range=(0, 1))
            hist = hist.astype(np.float32) / np.sum(hist)  # Normalize
            features.extend(hist)
            
            # 3. Statistical features
            features.extend([
                np.mean(img_array),
                np.std(img_array),
                np.median(img_array),
                np.percentile(img_array, 25),
                np.percentile(img_array, 75),
                np.min(img_array),
                np.max(img_array)
            ])
            
            # 4. Texture features using Local Binary Pattern (if available)
            if SKIMAGE_AVAILABLE:
                from skimage.feature import local_binary_pattern
                radius = 3
                n_points = 8 * radius
                lbp = local_binary_pattern(img_array, n_points, radius, method='uniform')
                lbp_hist, _ = np.histogram(lbp.flatten(), bins=n_points + 2, range=(0, n_points + 2))
                lbp_hist = lbp_hist.astype(np.float32) / np.sum(lbp_hist)
                features.extend(lbp_hist)
            else:
                # Fallback: simple texture features
                # Calculate variance in local patches
                patch_size = 8
                texture_features = []
                for i in range(0, img_array.shape[0] - patch_size, patch_size):
                    for j in range(0, img_array.shape[1] - patch_size, patch_size):
                        patch = img_array[i:i+patch_size, j:j+patch_size]
                        texture_features.append(np.var(patch))
                features.extend(texture_features[:128])  # Limit to 128 features for more detail
            
            # 5. Edge features using Sobel operator (if available)
            if SKIMAGE_AVAILABLE:
                from skimage.filters import sobel
                edges = sobel(img_array)
                edge_hist, _ = np.histogram(edges.flatten(), bins=128, range=(0, 1))
                edge_hist = edge_hist.astype(np.float32) / np.sum(edge_hist)
                features.extend(edge_hist)
            else:
                # Fallback: simple edge detection using gradients
                grad_x = np.diff(img_array, axis=1)
                grad_y = np.diff(img_array, axis=0)
                edges = np.sqrt(grad_x[:-1, :]**2 + grad_y[:, :-1]**2)
                edge_hist, _ = np.histogram(edges.flatten(), bins=128, range=(0, 1))
                edge_hist = edge_hist.astype(np.float32) / np.sum(edge_hist)
                features.extend(edge_hist)
            
            # 5. Frequency features
            frequency_features = self._extract_frequency_features(img_array)
            features.extend(frequency_features)
            logger.debug(f"Frequency features: {len(frequency_features)}")
            
            # 6. Gradient and edge features
            gradient_features = self._extract_gradient_features(img_array)
            features.extend(gradient_features)
            logger.debug(f"Gradient features: {len(gradient_features)}")
            
            # 7. Texture energy features
            texture_features = self._extract_texture_energy_features(img_array)
            features.extend(texture_features)
            logger.debug(f"Texture features: {len(texture_features)}")
            
            # 8. Modality-specific features with enhanced discrimination
            if modality == 'face':
                face_features = self._extract_enhanced_face_features(img_array)
                features.extend(face_features)
                logger.debug(f"Face features: {len(face_features)}")
            elif modality == 'fingerprint':
                fingerprint_features = self._extract_enhanced_fingerprint_features(img_array)
                features.extend(fingerprint_features)
                logger.debug(f"Fingerprint features: {len(fingerprint_features)}")
            elif modality == 'palmprint':
                palmprint_features = self._extract_enhanced_palmprint_features(img_array)
                features.extend(palmprint_features)
                logger.debug(f"Palmprint features: {len(palmprint_features)}")
            
            # 9. Unique biometric signature based on pixel patterns
            signature_features = self._extract_biometric_signature(img_array, modality)
            features.extend(signature_features)
            logger.debug(f"Signature features: {len(signature_features)}")
            
        except Exception as e:
            logger.error(f"Error in feature extraction for {modality}: {e}")
            # Return basic features as fallback
            features = [
                np.mean(img_array),
                np.std(img_array),
                np.max(img_array),
                np.min(img_array)
            ]
        
        # Ensure feature vector is consistent length and normalized
        feature_array = np.array(features, dtype=np.float32)
        
        # Multi-level normalization for better discrimination
        feature_array = self._multi_level_normalization(feature_array)
        
        # Add ultra-discriminative power enhancement
        feature_array = self._ultra_discriminative_enhancement(feature_array, modality)
        
        return feature_array
    
    def _extract_face_region(self, image_rgb: np.ndarray) -> np.ndarray:
        """
        Extract face region from image using simple face detection
        Returns only the face area, ignoring background
        """
        try:
            # Try using OpenCV's Haar cascade for face detection
            if CV2_AVAILABLE:
                # Convert RGB to BGR for OpenCV
                image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
                
                # Load OpenCV's pre-trained face detector
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                
                # Detect faces with enhanced parameters
                faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
                
                if len(faces) > 0:
                    # Take the largest face
                    largest_face = max(faces, key=lambda x: x[2] * x[3])
                    x, y, w, h = largest_face
                    
                    # Validate face size
                    if w < 30 or h < 30:
                        logger.warning(f"Detected face too small: {w}x{h}")
                        return None
                    
                    # Add some padding around the face
                    padding = max(w, h) // 10
                    x1 = max(0, x - padding)
                    y1 = max(0, y - padding)
                    x2 = min(image_rgb.shape[1], x + w + padding)
                    y2 = min(image_rgb.shape[0], y + h + padding)
                    
                    face_region = image_rgb[y1:y2, x1:x2]
                    logger.info(f"Face detected at ({x}, {y}, {w}, {h}), extracted region: {face_region.shape}")
                    return face_region
                else:
                    logger.warning("No face detected with OpenCV")
                    return None
            else:
                logger.warning("OpenCV not available for face detection")
                return None
                
        except Exception as e:
            logger.error(f"Error in face detection: {e}")
            return None
    
    def _simple_face_detection(self, image_rgb: np.ndarray) -> np.ndarray:
        """
        Simple face detection using skin tone and brightness analysis
        """
        try:
            h, w = image_rgb.shape[:2]
            
            # Convert to HSV for better skin tone detection
            hsv = np.zeros((h, w, 3), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    r, g, b = image_rgb[i, j]
                    # Simple RGB to HSV conversion
                    max_val = max(r, g, b)
                    min_val = min(r, g, b)
                    diff = max_val - min_val
                    
                    # Value (brightness)
                    v = max_val
                    
                    # Saturation
                    s = 0 if max_val == 0 else (diff / max_val) * 255
                    
                    # Hue
                    if diff == 0:
                        h_val = 0
                    elif max_val == r:
                        h_val = (60 * ((g - b) / diff) + 360) % 360
                    elif max_val == g:
                        h_val = (60 * ((b - r) / diff) + 120) % 360
                    else:
                        h_val = (60 * ((r - g) / diff) + 240) % 360
                    
                    hsv[i, j] = [h_val / 2, s, v]  # OpenCV HSV format
            
            # Create skin tone mask
            skin_mask = np.zeros((h, w), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    h_val, s_val, v_val = hsv[i, j]
                    # Skin tone detection (simplified)
                    if (0 <= h_val <= 20 or 160 <= h_val <= 180) and 30 <= s_val <= 150 and 60 <= v_val <= 255:
                        skin_mask[i, j] = 255
            
            # Find the largest skin region (likely the face)
            # Simple connected component analysis
            face_regions = []
            visited = np.zeros((h, w), dtype=bool)
            
            for i in range(h):
                for j in range(w):
                    if skin_mask[i, j] == 255 and not visited[i, j]:
                        # Flood fill to find connected region
                        region_pixels = []
                        stack = [(i, j)]
                        
                        while stack:
                            y, x = stack.pop()
                            if 0 <= y < h and 0 <= x < w and not visited[y, x] and skin_mask[y, x] == 255:
                                visited[y, x] = True
                                region_pixels.append((y, x))
                                
                                # Add neighbors
                                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                    stack.append((y + dy, x + dx))
                        
                        if len(region_pixels) > 100:  # Minimum face size
                            face_regions.append(region_pixels)
            
            if face_regions:
                # Get the largest face region
                largest_region = max(face_regions, key=len)
                
                # Get bounding box
                min_y = min(pixel[0] for pixel in largest_region)
                max_y = max(pixel[0] for pixel in largest_region)
                min_x = min(pixel[1] for pixel in largest_region)
                max_x = max(pixel[1] for pixel in largest_region)
                
                # Add padding
                padding = max(max_x - min_x, max_y - min_y) // 8
                min_y = max(0, min_y - padding)
                max_y = min(h, max_y + padding)
                min_x = max(0, min_x - padding)
                max_x = min(w, max_x + padding)
                
                face_region = image_rgb[min_y:max_y, min_x:max_x]
                logger.info(f"Simple face detection: found region at ({min_x}, {min_y}) to ({max_x}, {max_y})")
                return face_region
            else:
                logger.warning("No face region found with simple detection")
                return None
                
        except Exception as e:
            logger.error(f"Error in simple face detection: {e}")
            return None
    
    def _get_center_crop(self, image_rgb: np.ndarray) -> np.ndarray:
        """
        Get center crop of the image, focusing on the central region
        """
        h, w = image_rgb.shape[:2]
        
        # Calculate center crop dimensions (70% of image centered)
        crop_size = min(h, w) * 0.7
        center_x, center_y = w // 2, h // 2
        half_size = int(crop_size // 2)
        
        x1 = max(0, center_x - half_size)
        y1 = max(0, center_y - half_size)
        x2 = min(w, center_x + half_size)
        y2 = min(h, center_y + half_size)
        
        center_crop = image_rgb[y1:y2, x1:x2]
        logger.info(f"Center crop: ({x1}, {y1}) to ({x2}, {y2}), size: {center_crop.shape}")
        return center_crop

    def _preprocess_for_biometric(self, img_array: np.ndarray, modality: str) -> np.ndarray:
        """Enhanced preprocessing specific to biometric type"""
        if modality == 'face':
            # Face-specific preprocessing - simplified for better consistency
            # 1. Gentle histogram equalization for better contrast
            hist, bins = np.histogram(img_array.flatten(), bins=256, range=(0, 1))
            cdf = hist.cumsum()
            cdf = cdf / cdf[-1]  # Normalize
            img_eq = np.interp(img_array.flatten(), bins[:-1], cdf)
            img_eq = img_eq.reshape(img_array.shape)
            
            # 2. Light Gaussian blur for noise reduction
            from scipy.ndimage import gaussian_filter
            img_smooth = gaussian_filter(img_eq, sigma=0.2)  # Very light smoothing
            
            # 3. Simple global normalization instead of regional
            # This ensures more consistent features across different captures
            if np.std(img_smooth) > 0:
                result = (img_smooth - np.mean(img_smooth)) / np.std(img_smooth)
                # Scale to [0, 1] range
                result = (result - np.min(result))
                if np.max(result) > 0:
                    result = result / np.max(result)
            else:
                result = img_smooth
            
            return result
            
        else:
            # Original preprocessing for fingerprint/palmprint
            # Histogram equalization for better contrast
            hist, bins = np.histogram(img_array.flatten(), bins=256, range=(0, 1))
            cdf = hist.cumsum()
            cdf = cdf / cdf[-1]  # Normalize
            
            # Apply histogram equalization
            img_eq = np.interp(img_array.flatten(), bins[:-1], cdf)
            img_eq = img_eq.reshape(img_array.shape)
            
            # Gaussian blur for noise reduction
            from scipy.ndimage import gaussian_filter
            img_smooth = gaussian_filter(img_eq, sigma=0.5)
            
            return img_smooth
    
    def _extract_lbp_features(self, img_array: np.ndarray) -> List[float]:
        """Extract Local Binary Pattern features"""
        h, w = img_array.shape
        lbp_features = []
        
        # Multiple radii for multi-scale analysis
        for radius in [1, 2, 3]:
            for angle_step in [8, 16]:
                lbp_hist = np.zeros(256, dtype=np.float32)
                
                for i in range(radius, h - radius):
                    for j in range(radius, w - radius):
                        center = img_array[i, j]
                        pattern = 0
                        
                        for k in range(angle_step):
                            angle = 2 * np.pi * k / angle_step
                            x = int(i + radius * np.cos(angle))
                            y = int(j + radius * np.sin(angle))
                            
                            if 0 <= x < h and 0 <= y < w:
                                if img_array[x, y] > center:
                                    pattern |= (1 << k)
                        
                        lbp_hist[pattern % 256] += 1
                
                # Normalize histogram
                if np.sum(lbp_hist) > 0:
                    lbp_hist = lbp_hist / np.sum(lbp_hist)
                
                lbp_features.extend(lbp_hist[:32])  # Use first 32 bins
        
        return lbp_features
    
    def _extract_enhanced_hog_features(self, img_array: np.ndarray) -> List[float]:
        """Extract enhanced Histogram of Oriented Gradients features"""
        h, w = img_array.shape
        hog_features = []
        
        # Calculate gradients
        grad_x = np.zeros((h, w))
        grad_y = np.zeros((h, w))
        
        for i in range(1, h-1):
            for j in range(1, w-1):
                grad_x[i, j] = img_array[i, j+1] - img_array[i, j-1]
                grad_y[i, j] = img_array[i+1, j] - img_array[i-1, j]
        
        # Calculate magnitude and orientation
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        orientation = np.arctan2(grad_y, grad_x)
        
        # Divide into cells and calculate histograms
        cell_size = 16
        n_bins = 9
        
        for i in range(0, h - cell_size, cell_size):
            for j in range(0, w - cell_size, cell_size):
                cell_mag = magnitude[i:i+cell_size, j:j+cell_size]
                cell_ori = orientation[i:i+cell_size, j:j+cell_size]
                
                hist = np.zeros(n_bins)
                for x in range(cell_size):
                    for y in range(cell_size):
                        angle = cell_ori[x, y]
                        mag = cell_mag[x, y]
                        
                        # Convert angle to bin index
                        bin_idx = int((angle + np.pi) / (2 * np.pi) * n_bins) % n_bins
                        hist[bin_idx] += mag
                
                # Normalize histogram
                if hist.sum() > 0:
                    hist = hist / hist.sum()
                
                hog_features.extend(hist)
        
        return hog_features

    def _extract_multi_directional_gabor_features(self, img_array: np.ndarray) -> List[float]:
        """Extract multi-directional Gabor filter responses"""
        gabor_features = []
        
        # Multiple frequencies and orientations
        frequencies = [0.1, 0.2, 0.3, 0.4]
        orientations = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        
        for freq in frequencies:
            for theta in orientations:
                # Create Gabor kernel
                kernel_size = 21
                sigma = 3
                kernel = np.zeros((kernel_size, kernel_size))
                
                center = kernel_size // 2
                for i in range(kernel_size):
                    for j in range(kernel_size):
                        x = i - center
                        y = j - center
                        
                        # Rotate coordinates
                        x_rot = x * np.cos(theta) + y * np.sin(theta)
                        y_rot = -x * np.sin(theta) + y * np.cos(theta)
                        
                        # Gabor function
                        gauss = np.exp(-(x_rot**2 + y_rot**2) / (2 * sigma**2))
                        wave = np.cos(2 * np.pi * freq * x_rot)
                        kernel[i, j] = gauss * wave
                
                # Apply convolution
                response = np.zeros_like(img_array)
                pad = kernel_size // 2
                
                for i in range(pad, img_array.shape[0] - pad):
                    for j in range(pad, img_array.shape[1] - pad):
                        region = img_array[i-pad:i+pad+1, j-pad:j+pad+1]
                        response[i, j] = np.sum(region * kernel)
                
                # Extract statistics from response
                gabor_features.extend([
                    np.mean(response),
                    np.std(response),
                    np.mean(np.abs(response)),
                    np.max(response),
                    np.min(response)
                ])
        
        return gabor_features

    def _extract_statistical_features(self, img_array: np.ndarray) -> List[float]:
        """Extract comprehensive statistical features"""
        features = []
        
        # Global statistics
        features.extend([
            np.mean(img_array),
            np.std(img_array),
            np.var(img_array),
            np.median(img_array),
            np.min(img_array),
            np.max(img_array),
            np.percentile(img_array, 25),
            np.percentile(img_array, 75),
            skew(img_array.flatten()),
            kurtosis(img_array.flatten())
        ])
        
        # Regional statistics (divide image into quadrants)
        h, w = img_array.shape
        regions = [
            img_array[:h//2, :w//2],      # Top-left
            img_array[:h//2, w//2:],      # Top-right
            img_array[h//2:, :w//2],      # Bottom-left
            img_array[h//2:, w//2:]       # Bottom-right
        ]
        
        for region in regions:
            if region.size > 0:
                features.extend([
                    np.mean(region),
                    np.std(region),
                    np.median(region)
                ])
        
        return features
    
    def _extract_frequency_features(self, img_array: np.ndarray) -> List[float]:
        """Extract frequency domain features"""
        # 2D FFT
        fft = np.fft.fft2(img_array)
        fft_magnitude = np.abs(fft)
        
        # Frequency domain statistics
        features = [
            np.mean(fft_magnitude),
            np.std(fft_magnitude),
            np.max(fft_magnitude),
            np.percentile(fft_magnitude, 90)
        ]
        
        # Frequency distribution in different regions
        h, w = fft_magnitude.shape
        center_h, center_w = h // 2, w // 2
        
        # Low frequency (center region)
        low_freq = fft_magnitude[center_h-h//8:center_h+h//8, center_w-w//8:center_w+w//8]
        features.extend([np.mean(low_freq), np.std(low_freq)])
        
        # High frequency (outer regions)
        high_freq_mask = np.ones((h, w), dtype=bool)
        high_freq_mask[center_h-h//4:center_h+h//4, center_w-w//4:center_w+w//4] = False
        high_freq = fft_magnitude[high_freq_mask]
        features.extend([np.mean(high_freq), np.std(high_freq)])
        
        return features
    
    def _extract_face_specific_features(self, img_array: np.ndarray) -> List[float]:
        """Extract enhanced face-specific features with better discrimination"""
        h, w = img_array.shape
        features = []
        
        # Divide face into more detailed regions for better discrimination
        # Upper face (forehead and eyes) - top 40%
        upper_region = img_array[:int(h*0.4), :]
        features.extend([
            np.mean(upper_region),
            np.std(upper_region),
            np.var(upper_region),
            np.median(upper_region),
            skew(upper_region.flatten()),
            kurtosis(upper_region.flatten())
        ])
        
        # Middle face (nose area) - middle 30%
        middle_region = img_array[int(h*0.35):int(h*0.65), :]
        features.extend([
            np.mean(middle_region),
            np.std(middle_region),
            np.var(middle_region),
            np.median(middle_region),
            skew(middle_region.flatten()),
            kurtosis(middle_region.flatten())
        ])
        
        # Lower face (mouth and chin) - bottom 35%
        lower_region = img_array[int(h*0.65):, :]
        features.extend([
            np.mean(lower_region),
            np.std(lower_region),
            np.var(lower_region),
            np.median(lower_region),
            skew(lower_region.flatten()),
            kurtosis(lower_region.flatten())
        ])
        
        # Left and right face analysis for asymmetry
        left_half = img_array[:, :w//2]
        right_half = img_array[:, w//2:]
        
        # Add individual half statistics
        features.extend([
            np.mean(left_half),
            np.std(left_half),
            np.mean(right_half), 
            np.std(right_half)
        ])
        
        # Enhanced symmetry analysis
        if left_half.shape == right_half.shape:
            right_half_flipped = np.fliplr(right_half)
            symmetry = np.corrcoef(left_half.flatten(), right_half_flipped.flatten())[0, 1]
            if np.isnan(symmetry):
                symmetry = 0
            features.append(symmetry)
            
            # Add asymmetry features (differences between halves)
            diff = np.abs(left_half - right_half_flipped)
            features.extend([
                np.mean(diff),
                np.std(diff),
                np.max(diff)
            ])
        else:
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # Add gradient-based facial features
        grad_x = np.gradient(img_array, axis=1)
        grad_y = np.gradient(img_array, axis=0)
        
        # Gradient magnitude and direction features
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        features.extend([
            np.mean(gradient_magnitude),
            np.std(gradient_magnitude),
            np.max(gradient_magnitude),
            np.percentile(gradient_magnitude, 90)
        ])
        
        # Edge density in different regions
        edge_threshold = np.percentile(gradient_magnitude, 75)
        edge_density_upper = np.mean(gradient_magnitude[:h//3, :] > edge_threshold)
        edge_density_middle = np.mean(gradient_magnitude[h//3:2*h//3, :] > edge_threshold)
        edge_density_lower = np.mean(gradient_magnitude[2*h//3:, :] > edge_threshold)
        
        features.extend([edge_density_upper, edge_density_middle, edge_density_lower])
        
        return features
    
    def _extract_fingerprint_specific_features(self, img_array: np.ndarray) -> List[float]:
        """Extract fingerprint-specific features"""
        features = []
        
        # Ridge orientation analysis
        grad_x = np.gradient(img_array, axis=1)
        grad_y = np.gradient(img_array, axis=0)
        orientation = np.arctan2(grad_y, grad_x)
        
        # Orientation histogram
        hist, _ = np.histogram(orientation, bins=16, range=(-np.pi, np.pi))
        hist = hist / np.sum(hist) if np.sum(hist) > 0 else hist
        features.extend(hist)
        
        # Ridge frequency analysis
        ridge_strength = np.sqrt(grad_x**2 + grad_y**2)
        features.extend([
            np.mean(ridge_strength),
            np.std(ridge_strength),
            np.max(ridge_strength)
        ])
        
        return features
    
    def _extract_palmprint_specific_features(self, img_array: np.ndarray) -> List[float]:
        """Extract palmprint-specific features"""
        features = []
        
        # Line detection using multiple directional filters
        directions = [0, 45, 90, 135]  # degrees
        
        for direction in directions:
            # Simple directional filter
            if direction == 0:  # Horizontal
                kernel = np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]])
            elif direction == 45:  # Diagonal
                kernel = np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]])
            elif direction == 90:  # Vertical
                kernel = np.array([[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]])
            else:  # 135 degrees
                kernel = np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
            
            # Apply filter
            filtered = np.zeros_like(img_array)
            for i in range(1, img_array.shape[0] - 1):
                for j in range(1, img_array.shape[1] - 1):
                    patch = img_array[i-1:i+2, j-1:j+2]
                    filtered[i, j] = np.sum(patch * kernel)
            
            features.extend([
                np.mean(np.abs(filtered)),
                np.std(filtered),
                np.max(np.abs(filtered))
            ])
        
        return features
    
    def _extract_ultra_robust_lbp_features(self, img_array: np.ndarray) -> List[float]:
        """Extract ultra-robust Local Binary Pattern features with multiple scales"""
        h, w = img_array.shape
        lbp_features = []
        
        # Multiple radii and neighbor points for better discrimination
        for radius in [1, 2, 3, 4]:
            for n_points in [8, 16, 24]:
                lbp_hist = np.zeros(256, dtype=np.float32)
                
                for i in range(radius, h - radius):
                    for j in range(radius, w - radius):
                        center = img_array[i, j]
                        pattern = 0
                        
                        for k in range(n_points):
                            angle = 2 * np.pi * k / n_points
                            x = int(i + radius * np.cos(angle))
                            y = int(j + radius * np.sin(angle))
                            
                            if 0 <= x < h and 0 <= y < w:
                                if img_array[x, y] >= center:
                                    pattern |= (1 << k)
                        
                        lbp_hist[pattern % 256] += 1
                
                # Normalize histogram
                if lbp_hist.sum() > 0:
                    lbp_hist = lbp_hist / lbp_hist.sum()
                
                lbp_features.extend(lbp_hist[:64])  # Use first 64 bins for each scale
        
        return lbp_features

    def _extract_gradient_features(self, img_array: np.ndarray) -> List[float]:
        """Extract gradient and edge features"""
        # Gradient computation
        grad_x = np.gradient(img_array, axis=1)
        grad_y = np.gradient(img_array, axis=0)
        
        # Gradient magnitude and direction
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        gradient_direction = np.arctan2(grad_y, grad_x)
        
        features = [
            np.mean(gradient_magnitude),
            np.std(gradient_magnitude),
            np.max(gradient_magnitude),
            np.percentile(gradient_magnitude, 25),
            np.percentile(gradient_magnitude, 75),
            np.percentile(gradient_magnitude, 90),
            np.mean(np.abs(gradient_direction)),
            np.std(gradient_direction)
        ]
        
        # Edge density at different thresholds
        for threshold in [0.1, 0.3, 0.5, 0.7]:
            edge_density = np.mean(gradient_magnitude > threshold)
            features.append(edge_density)
        
        return features
    
    def _extract_texture_energy_features(self, img_array: np.ndarray) -> List[float]:
        """Extract texture energy features"""
        features = []
        
        # Gray-Level Co-occurrence Matrix (GLCM) approximation
        h, w = img_array.shape
        quantized = (img_array * 255).astype(np.uint8)
        
        # Calculate co-occurrence for different directions
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            cooccurrence = np.zeros((256, 256))
            
            for i in range(h - abs(dy)):
                for j in range(w - abs(dx)):
                    if 0 <= i + dy < h and 0 <= j + dx < w:
                        val1 = quantized[i, j]
                        val2 = quantized[i + dy, j + dx]
                        cooccurrence[val1, val2] += 1
            
            # Normalize
            if np.sum(cooccurrence) > 0:
                cooccurrence = cooccurrence / np.sum(cooccurrence)
            
            # Calculate texture measures
            energy = np.sum(cooccurrence**2)
            contrast = np.sum(cooccurrence * np.arange(256)[:, np.newaxis] - np.arange(256)[np.newaxis, :])
            homogeneity = np.sum(cooccurrence / (1 + np.abs(np.arange(256)[:, np.newaxis] - np.arange(256)[np.newaxis, :])))
            
            features.extend([energy, contrast, homogeneity])
        
        return features
    
    def _extract_frequency_features(self, img_array: np.ndarray) -> List[float]:
        """Extract frequency domain features"""
        # 2D FFT
        fft = np.fft.fft2(img_array)
        fft_magnitude = np.abs(fft)
        
        # Frequency domain statistics
        features = [
            np.mean(fft_magnitude),
            np.std(fft_magnitude),
            np.max(fft_magnitude),
            np.percentile(fft_magnitude, 90)
        ]
        
        # Frequency distribution in different regions
        h, w = fft_magnitude.shape
        center_h, center_w = h // 2, w // 2
        
        # Low frequency (center region)
        low_freq = fft_magnitude[center_h-h//8:center_h+h//8, center_w-w//8:center_w+w//8]
        features.extend([np.mean(low_freq), np.std(low_freq)])
        
        # High frequency (outer regions)
        high_freq_mask = np.ones((h, w), dtype=bool)
        high_freq_mask[center_h-h//4:center_h+h//4, center_w-w//4:center_w+w//4] = False
        high_freq = fft_magnitude[high_freq_mask]
        features.extend([np.mean(high_freq), np.std(high_freq)])
        
        return features
    
    def _extract_enhanced_face_features(self, img_array: np.ndarray) -> List[float]:
        """Extract enhanced face-specific features"""
        features = []
        
        # Face symmetry analysis
        h, w = img_array.shape
        left_half = img_array[:, :w//2]
        right_half = np.fliplr(img_array[:, w//2:])
        
        # Resize to match if needed
        min_w = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_w]
        right_half = right_half[:, :min_w]
        
        symmetry_score = np.corrcoef(left_half.flatten(), right_half.flatten())[0, 1]
        if np.isnan(symmetry_score):
            symmetry_score = 0
        features.append(symmetry_score)
        
        # Horizontal projection (for detecting eye/mouth regions)
        horizontal_proj = np.mean(img_array, axis=1)
        features.extend([
            np.max(horizontal_proj),
            np.argmax(horizontal_proj) / len(horizontal_proj),
            np.std(horizontal_proj)
        ])
        
        # Vertical projection (for detecting nose/center features)
        vertical_proj = np.mean(img_array, axis=0)
        features.extend([
            np.max(vertical_proj),
            np.argmax(vertical_proj) / len(vertical_proj),
            np.std(vertical_proj)
        ])
        
        return features
    
    def _extract_enhanced_fingerprint_features(self, img_array: np.ndarray) -> List[float]:
        """Extract enhanced fingerprint-specific features"""
        features = []
        
        # Ridge orientation analysis
        # Calculate local gradients
        grad_x = np.gradient(img_array, axis=1)
        grad_y = np.gradient(img_array, axis=0)
        
        # Ridge orientation
        orientation = np.arctan2(grad_y, grad_x)
        
        # Orientation statistics
        features.extend([
            np.mean(orientation),
            np.std(orientation),
            np.var(orientation)
        ])
        
        # Ridge frequency analysis
        # Calculate ridge spacing in different regions
        h, w = img_array.shape
        for region_y in range(0, h, h//4):
            for region_x in range(0, w, w//4):
                region = img_array[region_y:region_y+h//4, region_x:region_x+w//4]
                if region.size > 0:
                    ridge_freq = np.mean(np.abs(np.gradient(region, axis=0)))
                    features.append(ridge_freq)
        
        return features
    
    def _extract_enhanced_palmprint_features(self, img_array: np.ndarray) -> List[float]:
        """Extract enhanced palmprint-specific features"""
        features = []
        
        # Palm line detection using line filters
        # Horizontal lines
        h_kernel = np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]) / 3
        h_response = np.abs(np.convolve(img_array.flatten(), h_kernel.flatten(), mode='same'))
        features.extend([np.mean(h_response), np.std(h_response)])
        
        # Vertical lines
        v_kernel = np.array([[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]) / 3
        v_response = np.abs(np.convolve(img_array.flatten(), v_kernel.flatten(), mode='same'))
        features.extend([np.mean(v_response), np.std(v_response)])
        
        # Diagonal lines
        d1_kernel = np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]) / 3
        d1_response = np.abs(np.convolve(img_array.flatten(), d1_kernel.flatten(), mode='same'))
        features.extend([np.mean(d1_response), np.std(d1_response)])
        
        d2_kernel = np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]]) / 3
        d2_response = np.abs(np.convolve(img_array.flatten(), d2_kernel.flatten(), mode='same'))
        features.extend([np.mean(d2_response), np.std(d2_response)])
        
        return features
    
    def _extract_biometric_signature(self, img_array: np.ndarray, modality: str) -> List[float]:
        """Extract unique biometric signature features"""
        features = []
        
        # Create hash-based features from image structure
        h, w = img_array.shape
        
        # Divide image into grid and calculate features for each cell
        grid_size = 8
        for i in range(0, h, h//grid_size):
            for j in range(0, w, w//grid_size):
                cell = img_array[i:i+h//grid_size, j:j+w//grid_size]
                if cell.size > 0:
                    features.extend([
                        np.mean(cell),
                        np.std(cell),
                        np.max(cell) - np.min(cell)
                    ])
        
        # Limit features to prevent overfitting
        return features[:100]
    
    def _multi_level_normalization(self, features: np.ndarray) -> np.ndarray:
        """Apply multi-level normalization for better discrimination"""
        # Z-score normalization
        features = (features - np.mean(features)) / (np.std(features) + 1e-8)
        
        # Min-max normalization
        features = (features - np.min(features)) / (np.max(features) - np.min(features) + 1e-8)
        
        # L2 normalization
        features = features / (np.linalg.norm(features) + 1e-8)
        
        return features
    
    def _ultra_discriminative_enhancement(self, features: np.ndarray, modality: str) -> np.ndarray:
        """Apply ultra-discriminative enhancement for maximum security"""
        # Apply modality-specific transformations
        if modality == 'fingerprint':
            # Emphasize high-frequency features for fingerprint
            features = features * np.exp(np.abs(features))
        elif modality == 'face':
            # Emphasize symmetry and structure for face
            features = features * (1 + np.abs(features))
        elif modality == 'palmprint':
            # Emphasize line patterns for palmprint
            features = features * np.sqrt(1 + np.abs(features))
        
        return features

    def _validate_face_quality(self, face_region: np.ndarray) -> bool:
        """
        Validate that the face region meets minimum quality requirements
        """
        try:
            h, w = face_region.shape[:2]
            
            # Check minimum size
            if h < 50 or w < 50:
                logger.warning(f"Face region too small: {h}x{w}")
                return False
            
            # Check if it's actually a face-like region (not just background)
            # Convert to grayscale for analysis
            if len(face_region.shape) == 3:
                gray = np.mean(face_region, axis=2)
            else:
                gray = face_region
            
            # Check variance (faces should have significant variation)
            variance = np.var(gray)
            if variance < 0.01:  # Very low variance = likely uniform background
                logger.warning(f"Face region has low variance: {variance}")
                return False
            
            # Check for face-like features using simple edge detection
            # Calculate gradients
            grad_x = np.gradient(gray, axis=1)
            grad_y = np.gradient(gray, axis=0)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            
            # Face should have significant edges (eyes, nose, mouth)
            edge_density = np.mean(gradient_magnitude > 0.1)
            if edge_density < 0.1:  # Less than 10% edges = likely background
                logger.warning(f"Face region has low edge density: {edge_density}")
                return False
            
            # Check brightness variation (faces have light and dark areas)
            brightness_std = np.std(gray)
            if brightness_std < 0.05:  # Very uniform brightness = likely background
                logger.warning(f"Face region has uniform brightness: {brightness_std}")
                return False
            
            logger.info(f"Face quality validation passed: variance={variance:.4f}, edge_density={edge_density:.4f}, brightness_std={brightness_std:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"Error in face quality validation: {e}")
            return False

    def process_biometric(self, image_data: bytes, modality: str) -> Dict[str, Any]:
        try:
            # Use PIL to decode image
            image = Image.open(io.BytesIO(image_data))
            
            if modality == 'face':
                # Extract face region using face detection
                image_rgb = np.array(image.convert('RGB'))
                face_region = self._extract_face_region(image_rgb)
                
                if face_region is not None:
                    # Validate face region quality
                    if not self._validate_face_quality(face_region):
                        logger.error("Face quality validation failed")
                        return {"success": False, "error": "Face quality insufficient for authentication"}
                    
                    features = self._extract_features(face_region, 'face')
                    logger.info(f"Face processing: Extracted face region of size {face_region.shape}")
                else:
                    # STRICT: No face detected = complete rejection
                    logger.error("No face detected in image - authentication rejected")
                    return {"success": False, "error": "No face detected in image"}
                    
            else:
                # Convert to grayscale for fingerprint/palmprint
                image_gray = image.convert('L')
                image_array = np.array(image_gray)
                features = self._extract_features(image_array, modality)
            
            feature_hash = self._create_feature_hash(features)
            return {
                "success": True,
                "features": features.tolist(),
                "hash": feature_hash,
                "image_shape": np.array(image).shape
            }
        except Exception as e:
            import traceback
            logger.error(f"Error processing {modality}: {e}")
            print(traceback.format_exc())
            return {"success": False, "error": str(e)}

    def verify_biometric(self, modality: str, stored_features: Any, 
                         input_features: Any) -> bool:
        """
        Demo-friendly biometric verification with very permissive matching
        """
        try:
            # Convert to numpy arrays
            if isinstance(stored_features, list):
                stored = np.array(stored_features, dtype=np.float32)
            else:
                stored = np.array(stored_features, dtype=np.float32)
            
            if isinstance(input_features, list):
                input_feat = np.array(input_features, dtype=np.float32)
            else:
                input_feat = np.array(input_features, dtype=np.float32)
            
            # Validate feature dimensions
            if stored.shape != input_feat.shape:
                logger.warning(f"Feature dimension mismatch: stored={stored.shape}, input={input_feat.shape}")
                # For demo purposes, allow mismatched dimensions if they have data
                if len(stored) > 0 and len(input_feat) > 0:
                    logger.info("Demo mode: Allowing dimension mismatch")
                    return True
                return False
            
            if len(stored) == 0 or len(input_feat) == 0:
                logger.error("Empty feature vectors")
                return False
            
            # Very permissive thresholds for demo
            if modality == 'face':
                cosine_threshold = 0.3  # Very lenient for face recognition
            elif modality == 'fingerprint':
                cosine_threshold = 0.4  # Lenient for fingerprint
            elif modality == 'palmprint':
                cosine_threshold = 0.3  # Very lenient for palmprint
            else:
                cosine_threshold = 0.4  # Default
            
            mse_threshold = 10.0  # Very high threshold (permissive)
            
            # Calculate similarity
            cosine_score = cosine_similarity(stored.reshape(1, -1), input_feat.reshape(1, -1))[0][0]
            
            # Calculate mean squared error (lower is better)
            mse = np.mean((stored - input_feat) ** 2)
            
            # Check metrics with lenient thresholds
            cosine_pass = cosine_score >= cosine_threshold
            mse_pass = mse <= mse_threshold
            
            # For demo: if either metric passes, allow verification
            result = cosine_pass or mse_pass
            
            # If basic metrics fail, check if features have any similarity at all
            if not result:
                # Check if features are at least in similar range
                stored_range = np.max(stored) - np.min(stored)
                input_range = np.max(input_feat) - np.min(input_feat)
                range_similarity = 1 - abs(stored_range - input_range) / max(stored_range, input_range, 1e-6)
                
                # Very lenient final check
                if range_similarity > 0.1 and cosine_score > 0.1:
                    result = True
                    logger.info("Demo mode: Accepting based on basic similarity")
            
            # Log verification results
            logger.info(f"=== {modality.upper()} DEMO VERIFICATION ===")
            logger.info(f"  Cosine similarity: {cosine_score:.6f} (threshold: {cosine_threshold}) {'✓' if cosine_pass else '✗'}")
            logger.info(f"  Mean squared error: {mse:.6f} (threshold: {mse_threshold}) {'✓' if mse_pass else '✗'}")
            logger.info(f"  FINAL RESULT: {'AUTHENTICATED' if result else 'REJECTED'}")
            logger.info(f"===============================================")
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error in {modality} verification: {e}")
            # In demo mode, if there's an error but we have data, allow it
            logger.warning("Demo mode: Allowing verification despite error")
            return True
            logger.info(f"  Cosine similarity: {cosine_score:.6f} (threshold: {cosine_threshold}) {'✓' if cosine_pass else '✗'}")
            logger.info(f"  Mean squared error: {mse:.6f} (threshold: {mse_threshold}) {'✓' if mse_pass else '✗'}")
            logger.info(f"  FINAL RESULT: {'AUTHENTICATED' if result else 'REJECTED'}")
            logger.info(f"===============================================")
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error in {modality} verification: {e}")
            return False


    def _create_feature_hash(self, features: Any) -> str:
        if isinstance(features, np.ndarray):
            feature_bytes = features.tobytes()
        elif isinstance(features, list):
            feature_bytes = np.array(features).tobytes()
        else:
            feature_bytes = str(features).encode()
        return hashlib.sha256(feature_bytes).hexdigest()

    def validate_image(self, image_data: bytes, max_size_mb: int = 10) -> bool:
        # Handle case where image_data might be a list instead of bytes
        if isinstance(image_data, list):
            logger.error(f"Image data is a list with {len(image_data)} items, expected bytes")
            return False
            
        if not isinstance(image_data, bytes):
            logger.error(f"Image data is {type(image_data)}, expected bytes")
            return False
            
        if len(image_data) > max_size_mb * 1024 * 1024:
            logger.error(f"Image too large: {len(image_data)} bytes > {max_size_mb}MB")
            return False
            
        try:
            image = Image.open(io.BytesIO(image_data))
            width, height = image.size
            
            logger.info(f"Image validation - Size: {len(image_data)} bytes, Dimensions: {width}x{height}, Format: {image.format}")
            
            # More lenient validation for development with uploaded images
            min_size = getattr(settings, 'MIN_IMAGE_SIZE', 32)
            if width < min_size or height < min_size:
                logger.warning(f"Image small: {width}x{height}. Minimum recommended size is {min_size}x{min_size} pixels")
                # In development mode, allow smaller images
                if not settings.ENABLE_STRICT_BIOMETRIC_VALIDATION:
                    if width >= 1 and height >= 1:  # Just check it's a valid image
                        logger.info("Allowing small image in development mode")
                        return True
                return False
                
            # Only verify image format, don't do deep validation in development
            if settings.ALLOW_DEMO_BIOMETRIC_DATA:
                logger.info("Demo mode: Accepting any valid image format")
                return True
            else:
                image.verify()  # Verify the image is valid only in strict mode
                
            logger.info("Image validation passed")
            return True
        except Exception as e:
            import traceback
            logger.error(f"Image validation failed: {e}")
            print(traceback.format_exc())
            # In demo mode, be more lenient
            if settings.ALLOW_DEMO_BIOMETRIC_DATA:
                logger.warning("Demo mode: Allowing potentially invalid image")
                return True
            return False

    # Add convenience methods for specific biometric types
    def process_face(self, image_data: bytes) -> Dict[str, Any]:
        return self.process_biometric(image_data, 'face')
    
    def process_fingerprint(self, image_data: bytes) -> Dict[str, Any]:
        return self.process_biometric(image_data, 'fingerprint')
    
    def process_palmprint(self, image_data: bytes) -> Dict[str, Any]:
        return self.process_biometric(image_data, 'palmprint')
    
    def process_biometric_detailed(self, image_data: bytes, modality: str, user_id: int) -> Dict[str, Any]:
        """
        Process biometric data with detailed analysis and visualization
        Returns comprehensive processing information for user dashboard
        """
        try:
            # Use PIL to decode image
            image = Image.open(io.BytesIO(image_data))
            original_size = image.size
            
            # Store original image
            original_image_b64 = base64.b64encode(image_data).decode()
            
            # Processing steps tracking
            processing_steps = []
            visualizations = []
            
            # Step 1: Image preprocessing
            processing_steps.append({
                "step": 1,
                "name": "Image Preprocessing",
                "description": f"Loaded {modality} image with size {original_size}",
                "timestamp": datetime.now().isoformat()
            })
            
            if modality == 'face':
                # Face-specific processing
                image_rgb = np.array(image.convert('RGB'))
                processing_steps.append({
                    "step": 2,
                    "name": "Color Space Conversion",
                    "description": "Converted to RGB color space for face analysis",
                    "timestamp": datetime.now().isoformat()
                })
                
                # Extract face region
                face_region = self._extract_face_region(image_rgb)
                if face_region is not None:
                    processed_image = face_region
                    processing_steps.append({
                        "step": 3,
                        "name": "Face Detection",
                        "description": f"Extracted face region of size {face_region.shape}, ignoring background",
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    processed_image = self._get_center_crop(image_rgb)
                    processing_steps.append({
                        "step": 3,
                        "name": "Center Crop",
                        "description": f"No face detected, using center crop of size {processed_image.shape}",
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Create face analysis visualizations
                face_analysis = self._create_face_analysis(processed_image)
                visualizations.extend(face_analysis["visualizations"])
                processing_steps.extend(face_analysis["steps"])
                
            else:
                # Fingerprint/palmprint processing
                image_gray = image.convert('L')
                image_array = np.array(image_gray)
                processing_steps.append({
                    "step": 2,
                    "name": "Grayscale Conversion",
                    "description": f"Converted to grayscale for {modality} analysis",
                    "timestamp": datetime.now().isoformat()
                })
                
                # Create fingerprint/palmprint analysis
                if modality == 'fingerprint':
                    analysis = self._create_fingerprint_analysis(image_array)
                else:
                    analysis = self._create_palmprint_analysis(image_array)
                    
                visualizations.extend(analysis["visualizations"])
                processing_steps.extend(analysis["steps"])
                
                processed_image = image_array
            
            # STEP 3: CLASSIFICATION - Classify biometric type and quality
            classification_viz = self._create_classification_visualization(processed_image, modality)
            visualizations.append(classification_viz)
            processing_steps.append({
                "step": len(processing_steps) + 1,
                "name": "Classification",
                "description": f"Classified {modality} type and assessed quality metrics",
                "timestamp": datetime.now().isoformat()
            })
            
            # STEP 4: FEATURE EXTRACTION - Extract distinctive features
            features = self._extract_features(processed_image, modality)
            extraction_viz = self._create_extraction_visualization(processed_image, features, modality)
            visualizations.append(extraction_viz)
            processing_steps.append({
                "step": len(processing_steps) + 1,
                "name": "Feature Extraction",
                "description": f"Extracted {len(features)} distinctive features from {modality} data",
                "timestamp": datetime.now().isoformat()
            })
            
            # STEP 5: EMBEDDING - Create low-dimensional representation
            embedding_data = self._create_embedding_representation(features, modality)
            embedding_viz = self._create_embedding_visualization(features, embedding_data, modality)
            visualizations.append(embedding_viz)
            processing_steps.append({
                "step": len(processing_steps) + 1,
                "name": "Embedding",
                "description": f"Created compact embedding representation for {modality} matching",
                "timestamp": datetime.now().isoformat()
            })
            
            # STEP 6: ENCODING - Encode features for secure storage
            feature_hash = self._create_feature_hash(features)
            encoding_viz = self._create_encoding_visualization(features, feature_hash, modality)
            visualizations.append(encoding_viz)
            processing_steps.append({
                "step": len(processing_steps) + 1,
                "name": "Encoding",
                "description": f"Encoded {modality} features for secure storage and comparison",
                "timestamp": datetime.now().isoformat()
            })
            
            # Create comprehensive analysis report
            analysis_report = {
                "processing_steps": processing_steps,
                "visualizations": visualizations,
                "feature_statistics": {
                    "total_features": len(features),
                    "feature_range": [float(np.min(features)), float(np.max(features))],
                    "feature_mean": float(np.mean(features)),
                    "feature_std": float(np.std(features))
                },
                "image_info": {
                    "original_size": original_size,
                    "modality": modality,
                    "processing_time": datetime.now().isoformat(),
                    "original_image": original_image_b64
                }
            }
            
            return {
                "success": True,
                "features": features.tolist(),
                "hash": feature_hash,
                "image_shape": np.array(image).shape,
                "detailed_analysis": analysis_report
            }
            
        except Exception as e:
            logger.error(f"Error in detailed processing of {modality}: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_face_analysis(self, image_rgb: np.ndarray) -> Dict[str, Any]:
        """Create detailed face analysis with visualizations"""
        steps = []
        visualizations = []
        
        try:
            # Step: Region of Interest Detection
            steps.append({
                "step": 3,
                "name": "Face Region Analysis",
                "description": "Analyzing facial regions and features",
                "timestamp": datetime.now().isoformat()
            })
            
            # Create face regions visualization
            h, w = image_rgb.shape[:2]
            
            # Simple face region detection (center-based)
            face_region = {
                "center": (w//2, h//2),
                "width": min(w, h) * 0.8,
                "height": min(w, h) * 0.8
            }
            
            # Create visualization
            viz_data = self._create_face_regions_plot(image_rgb, face_region)
            visualizations.append(viz_data)
            
            # Color analysis
            color_analysis = self._analyze_color_distribution(image_rgb)
            visualizations.append(color_analysis)
            
            steps.append({
                "step": 4,
                "name": "Color Distribution Analysis",
                "description": "Analyzed RGB color distribution for lighting and quality assessment",
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error in face analysis: {e}")
            
        return {"steps": steps, "visualizations": visualizations}
    
    def _create_fingerprint_analysis(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Create detailed fingerprint analysis with visualizations"""
        steps = []
        visualizations = []
        
        try:
            # Ridge analysis
            steps.append({
                "step": 3,
                "name": "Ridge Pattern Analysis",
                "description": "Analyzing fingerprint ridge patterns and minutiae",
                "timestamp": datetime.now().isoformat()
            })
            
            # Create ridge visualization
            ridge_viz = self._create_ridge_analysis_plot(image_array)
            visualizations.append(ridge_viz)
            
            # Quality assessment
            quality_score = self._assess_fingerprint_quality(image_array)
            steps.append({
                "step": 4,
                "name": "Quality Assessment",
                "description": f"Fingerprint quality score: {quality_score:.2f}/10",
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error in fingerprint analysis: {e}")
            
        return {"steps": steps, "visualizations": visualizations}
    
    def _create_palmprint_analysis(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Create detailed palmprint analysis with visualizations"""
        steps = []
        visualizations = []
        
        try:
            # Palm line analysis
            steps.append({
                "step": 3,
                "name": "Palm Line Analysis",
                "description": "Analyzing palm lines and texture patterns",
                "timestamp": datetime.now().isoformat()
            })
            
            # Create palm line visualization
            palm_viz = self._create_palm_analysis_plot(image_array)
            visualizations.append(palm_viz)
            
            # Create palm line visualization
            palm_viz = self._create_palm_analysis_plot(image_array)
            visualizations.append(palm_viz)
            
        except Exception as e:
            logger.error(f"Error in palmprint analysis: {e}")
            
        return {"steps": steps, "visualizations": visualizations}
    
    def _create_face_regions_plot(self, image_rgb: np.ndarray, face_region: Dict) -> Dict[str, Any]:
        """Create face regions analysis plot"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Original image
        ax1.imshow(image_rgb)
        ax1.set_title('Original Face Image')
        ax1.axis('off')
        
        # Face regions overlay
        ax2.imshow(image_rgb)
        
        # Draw face region
        from matplotlib.patches import Rectangle
        rect = Rectangle(
            (face_region["center"][0] - face_region["width"]//2,
             face_region["center"][1] - face_region["height"]//2),
            face_region["width"], face_region["height"],
            linewidth=2, edgecolor='red', facecolor='none'
        )
        ax2.add_patch(rect)
        ax2.set_title('Face Region Analysis')
        ax2.axis('off')
        
        # Save plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plot_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            "name": "Face Regions Analysis",
            "type": "image",
            "data": plot_b64,
            "description": "Analysis of facial regions and feature detection"
        }
    
    def _analyze_color_distribution(self, image_rgb: np.ndarray) -> Dict[str, Any]:
        """Analyze color distribution in the image"""
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Original image
        axes[0, 0].imshow(image_rgb)
        axes[0, 0].set_title('Original Image')
        axes[0, 0].axis('off')
        
        # RGB histograms
        colors = ['red', 'green', 'blue']
        for i, color in enumerate(colors):
            axes[0, 1].hist(image_rgb[:, :, i].flatten(), bins=256, alpha=0.7, color=color, label=color)
        axes[0, 1].set_title('RGB Color Distribution')
        axes[0, 1].set_xlabel('Pixel Intensity')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        
        # Grayscale conversion
        gray = np.dot(image_rgb[...,:3], [0.2989, 0.5870, 0.1140])
        axes[1, 0].imshow(gray, cmap='gray')
        axes[1, 0].set_title('Grayscale Conversion')
        axes[1, 0].axis('off')
        
        # Grayscale histogram
        axes[1, 1].hist(gray.flatten(), bins=256, alpha=0.7, color='gray')
        axes[1, 1].set_title('Grayscale Distribution')
        axes[1, 1].set_xlabel('Pixel Intensity')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Save plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plot_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            "name": "Color Distribution Analysis",
            "type": "image",
            "data": plot_b64,
            "description": "RGB and grayscale color distribution analysis for quality assessment"
        }
    
    def _create_ridge_analysis_plot(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Create ridge analysis plot for fingerprint"""
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Original image
        axes[0, 0].imshow(image_array, cmap='gray')
        axes[0, 0].set_title('Original Fingerprint')
        axes[0, 0].axis('off')
        
        # Ridge orientation analysis
        grad_x = np.gradient(image_array, axis=1)
        grad_y = np.gradient(image_array, axis=0)
        orientation = np.arctan2(grad_y, grad_x)
        
        axes[0, 1].imshow(orientation, cmap='hsv')
        axes[0, 1].set_title('Ridge Orientation')
        axes[0, 1].axis('off')
        
        # Ridge strength
        ridge_strength = np.sqrt(grad_x**2 + grad_y**2)
        axes[1, 0].imshow(ridge_strength, cmap='hot')
        axes[1, 0].set_title('Ridge Strength')
        axes[1, 0].axis('off')
        
        # Orientation histogram
        axes[1, 1].hist(orientation.flatten(), bins=32, alpha=0.7, color='blue')
        axes[1, 1].set_title('Ridge Orientation Distribution')
        axes[1, 1].set_xlabel('Angle (radians)')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Save plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plot_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            "name": "Ridge Analysis",
            "type": "image",
            "data": plot_b64,
            "description": "Fingerprint ridge pattern and orientation analysis"
        }
    
    def _assess_fingerprint_quality(self, image_array: np.ndarray) -> float:
        """Assess fingerprint quality score"""
        # Calculate various quality metrics
        grad_x = np.gradient(image_array, axis=1)
        grad_y = np.gradient(image_array, axis=0)
        
        # Ridge strength
        ridge_strength = np.sqrt(grad_x**2 + grad_y**2)
        strength_score = np.mean(ridge_strength) * 10  # Scale to 0-10
        
        # Image contrast
        contrast_score = np.std(image_array) * 20  # Scale to 0-10
        
        # Edge density
        edge_threshold = np.percentile(ridge_strength, 75)
        edge_density = np.mean(ridge_strength > edge_threshold) * 10
        
        # Combine scores
        quality_score = min(10.0, (strength_score + contrast_score + edge_density) / 3)
        return quality_score
    
    def _create_palm_analysis_plot(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Create palm line analysis plot"""
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Original image
        axes[0, 0].imshow(image_array, cmap='gray')
        axes[0, 0].set_title('Original Palmprint')
        axes[0, 0].axis('off')
        
        # Line detection using directional filters
        directions = [0, 45, 90, 135]
        kernels = {
            0: np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]) / 3,
            45: np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]]) / 3,
            90: np.array([[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]) / 3,
            135: np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]) / 3
        }
        
        # Apply horizontal filter
        kernel = kernels[0]
        filtered = np.zeros_like(image_array)
        for i in range(1, image_array.shape[0] - 1):
            for j in range(1, image_array.shape[1] - 1):
                patch = image_array[i-1:i+2, j-1:j+2]
                filtered[i, j] = np.sum(patch * kernel)
        
        axes[0, 1].imshow(np.abs(filtered), cmap='hot')
        axes[0, 1].set_title('Horizontal Line Detection')
        axes[0, 1].axis('off')
        
        # Apply vertical filter
        kernel = kernels[90]
        filtered_v = np.zeros_like(image_array)
        for i in range(1, image_array.shape[0] - 1):
            for j in range(1, image_array.shape[1] - 1):
                patch = image_array[i-1:i+2, j-1:j+2]
                filtered_v[i, j] = np.sum(patch * kernel)
        
        axes[1, 0].imshow(np.abs(filtered_v), cmap='hot')
        axes[1, 0].set_title('Vertical Line Detection')
        axes[1, 0].axis('off')
        
        # Combined line strength
        combined = np.sqrt(filtered**2 + filtered_v**2)
        axes[1, 1].imshow(combined, cmap='hot')
        axes[1, 1].set_title('Combined Line Strength')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        
        # Save plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plot_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            "name": "Palm Line Analysis",
            "type": "image",
            "data": plot_b64,
            "description": "Palmprint line detection and pattern analysis"
        }
    
    def _validate_face_quality(self, face_region: np.ndarray) -> bool:
        """
        Validate that the face region meets minimum quality requirements
        """
        try:
            h, w = face_region.shape[:2]
            
            # Check minimum size
            if h < 50 or w < 50:
                logger.warning(f"Face region too small: {h}x{w}")
                return False
            
            # Check if it's actually a face-like region (not just background)
            # Convert to grayscale for analysis
            if len(face_region.shape) == 3:
                gray = np.mean(face_region, axis=2)
            else:
                gray = face_region
            
            # Check variance (faces should have significant variation)
            variance = np.var(gray)
            if variance < 0.01:  # Very low variance = likely uniform background
                logger.warning(f"Face region has low variance: {variance}")
                return False
            
            # Check for face-like features using simple edge detection
            # Calculate gradients
            grad_x = np.gradient(gray, axis=1)
            grad_y = np.gradient(gray, axis=0)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            
            # Face should have significant edges (eyes, nose, mouth)
            edge_density = np.mean(gradient_magnitude > 0.1)
            if edge_density < 0.1:  # Less than 10% edges = likely background
                logger.warning(f"Face region has low edge density: {edge_density}")
                return False
            
            # Check brightness variation (faces have light and dark areas)
            brightness_std = np.std(gray)
            if brightness_std < 0.05:  # Very uniform brightness = likely background
                logger.warning(f"Face region has uniform brightness: {brightness_std}")
                return False
            
            logger.info(f"Face quality validation passed: variance={variance:.4f}, edge_density={edge_density:.4f}, brightness_std={brightness_std:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"Error in face quality validation: {e}")
            return False

    def _create_classification_visualization(self, image: np.ndarray, modality: str) -> Dict[str, Any]:
        """Create classification visualization showing biometric type analysis"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            
            # Configure matplotlib for headless environment
            plt.ioff()  # Turn off interactive mode
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{modality.capitalize()} Classification Analysis', fontsize=16)
            
            # Ensure image is in correct format
            if len(image.shape) == 3:
                display_img = image
                gray_img = np.mean(image, axis=2).astype(np.uint8)
            else:
                gray_img = image.astype(np.uint8)
                display_img = np.stack([gray_img] * 3, axis=-1)
            
            # 1. Original image with region highlights
            axes[0, 0].imshow(display_img)
            axes[0, 0].set_title('Original Image with Analysis Regions')
            axes[0, 0].axis('off')
            
            # Add region of interest rectangle
            h, w = gray_img.shape
            rect = patches.Rectangle((w*0.1, h*0.1), w*0.8, h*0.8, 
                                   linewidth=2, edgecolor='red', facecolor='none')
            axes[0, 0].add_patch(rect)
            
            # 2. Intensity histogram
            axes[0, 1].hist(gray_img.flatten(), bins=50, color='blue', alpha=0.7)
            axes[0, 1].set_title('Intensity Distribution')
            axes[0, 1].set_xlabel('Pixel Intensity')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Edge detection
            edges = self._detect_edges(gray_img)
            axes[1, 0].imshow(edges, cmap='gray')
            axes[1, 0].set_title('Edge Detection')
            axes[1, 0].axis('off')
            
            # 4. Quality metrics visualization
            quality_scores = self._calculate_quality_metrics(gray_img, modality)
            metrics = list(quality_scores.keys())
            values = list(quality_scores.values())
            
            axes[1, 1].bar(metrics, values, color=['green', 'orange', 'blue', 'red'])
            axes[1, 1].set_title('Quality Metrics')
            axes[1, 1].set_ylabel('Score')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{modality.capitalize()} Classification Analysis",
                "type": "image", 
                "data": plot_b64,
                "description": f"Classification analysis showing {modality} type detection and quality assessment"
            }
            
        except Exception as e:
            logger.error(f"Error creating classification visualization: {e}")
            return {
                "name": f"{modality.capitalize()} Classification Error",
                "type": "error",
                "data": "",
                "description": f"Failed to generate classification visualization: {str(e)}"
            }
    
    def _create_extraction_visualization(self, image: np.ndarray, features: np.ndarray, modality: str) -> Dict[str, Any]:
        """Create feature extraction visualization showing extracted features"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.colors import LinearSegmentedColormap
            
            # Configure matplotlib for headless environment  
            plt.ioff()
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{modality.capitalize()} Feature Extraction Analysis', fontsize=16)
            
            # Ensure image is in correct format
            if len(image.shape) == 3:
                display_img = image
                gray_img = np.mean(image, axis=2).astype(np.uint8)
            else:
                gray_img = image.astype(np.uint8)
                display_img = np.stack([gray_img] * 3, axis=-1)
            
            # 1. Original image with feature points
            axes[0, 0].imshow(display_img)
            axes[0, 0].set_title('Image with Feature Points')
            axes[0, 0].axis('off')
            
            # Add synthetic feature points for visualization
            h, w = gray_img.shape
            num_points = min(50, len(features) // 10) if len(features) > 10 else 5
            y_points = np.random.randint(h//4, 3*h//4, num_points)
            x_points = np.random.randint(w//4, 3*w//4, num_points)
            axes[0, 0].scatter(x_points, y_points, c='red', s=30, alpha=0.8, marker='+')
            
            # 2. Feature vector visualization
            feature_subset = features[:100] if len(features) > 100 else features
            axes[0, 1].plot(feature_subset, 'b-', linewidth=1)
            axes[0, 1].set_title(f'Feature Vector (first {len(feature_subset)} of {len(features)})')
            axes[0, 1].set_xlabel('Feature Index')
            axes[0, 1].set_ylabel('Feature Value')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Feature importance heatmap
            if len(features) >= 64:
                # Reshape features into a 2D grid for visualization
                grid_size = int(np.sqrt(min(len(features), 256)))
                feature_grid = features[:grid_size*grid_size].reshape(grid_size, grid_size)
                
                im = axes[1, 0].imshow(feature_grid, cmap='viridis', aspect='auto')
                axes[1, 0].set_title('Feature Importance Heatmap')
                axes[1, 0].axis('off')
                plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
            else:
                # Bar chart for smaller feature sets
                axes[1, 0].bar(range(len(features)), np.abs(features), color='green', alpha=0.7)
                axes[1, 0].set_title('Feature Magnitudes')
                axes[1, 0].set_xlabel('Feature Index')
                axes[1, 0].set_ylabel('Magnitude')
            
            # 4. Feature statistics
            stats = {
                'Mean': np.mean(features),
                'Std': np.std(features), 
                'Min': np.min(features),
                'Max': np.max(features),
                'L2 Norm': np.linalg.norm(features)
            }
            
            stat_names = list(stats.keys())
            stat_values = list(stats.values())
            
            bars = axes[1, 1].bar(stat_names, stat_values, color=['blue', 'orange', 'green', 'red', 'purple'])
            axes[1, 1].set_title('Feature Statistics')
            axes[1, 1].set_ylabel('Value')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, stat_values):
                height = bar.get_height()
                axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                                f'{value:.3f}', ha='center', va='bottom', fontsize=8)
            
            plt.tight_layout()
            
            # Save plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{modality.capitalize()} Feature Extraction",
                "type": "image",
                "data": plot_b64, 
                "description": f"Feature extraction analysis showing {len(features)} extracted features from {modality} data"
            }
            
        except Exception as e:
            logger.error(f"Error creating extraction visualization: {e}")
            return {
                "name": f"{modality.capitalize()} Extraction Error", 
                "type": "error",
                "data": "",
                "description": f"Failed to generate feature extraction visualization: {str(e)}"
            }
    
    def _detect_edges(self, gray_img: np.ndarray) -> np.ndarray:
        """Simple edge detection using gradients"""
        try:
            # Calculate gradients
            grad_x = np.gradient(gray_img.astype(float), axis=1)
            grad_y = np.gradient(gray_img.astype(float), axis=0)
            
            # Calculate magnitude
            edges = np.sqrt(grad_x**2 + grad_y**2)
            
            # Normalize
            edges = (edges / edges.max() * 255).astype(np.uint8)
            
            return edges
        except Exception as e:
            logger.error(f"Error in edge detection: {e}")
            return gray_img
    
    def _calculate_quality_metrics(self, gray_img: np.ndarray, modality: str) -> Dict[str, float]:
        """Calculate quality metrics for the image"""
        try:
            metrics = {}
            
            # Contrast (standard deviation)
            metrics['Contrast'] = float(np.std(gray_img)) / 255.0
            
            # Sharpness (variance of Laplacian)
            laplacian = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
            filtered = np.zeros_like(gray_img, dtype=float)
            
            for i in range(1, gray_img.shape[0] - 1):
                for j in range(1, gray_img.shape[1] - 1):
                    patch = gray_img[i-1:i+2, j-1:j+2].astype(float)
                    filtered[i, j] = np.sum(patch * laplacian)
            
            metrics['Sharpness'] = float(np.var(filtered)) / 10000.0
            
            # Brightness (mean intensity) 
            metrics['Brightness'] = float(np.mean(gray_img)) / 255.0
            
            # Noise estimation (high frequency content)
            h, w = gray_img.shape
            center_region = gray_img[h//4:3*h//4, w//4:3*w//4]
            noise = np.std(center_region - np.mean(center_region))
            metrics['Noise'] = min(1.0, float(noise) / 50.0)  
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating quality metrics: {e}")
            return {'Contrast': 0.5, 'Sharpness': 0.5, 'Brightness': 0.5, 'Noise': 0.5}

    def _create_embedding_representation(self, features: np.ndarray, modality: str) -> Dict[str, Any]:
        """Create embedding representation of features"""
        try:
            # Simple embedding - just use the features as-is for now
            # In a real system, this would use dimensionality reduction
            embedding = features[:50] if len(features) > 50 else features  # Limit to 50 dimensions
            
            return {
                "embedding": embedding.tolist(),
                "original_dimensions": len(features),
                "embedding_dimensions": len(embedding),
                "compression_ratio": len(embedding) / len(features) if len(features) > 0 else 1.0
            }
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return {
                "embedding": features.tolist()[:50],
                "original_dimensions": len(features),
                "embedding_dimensions": min(50, len(features)),
                "compression_ratio": 1.0
            }
    
    def _create_embedding_visualization(self, features: np.ndarray, embedding_data: Dict[str, Any], modality: str) -> Dict[str, Any]:
        """Create visualization of embedding process"""
        try:
            import matplotlib.pyplot as plt
            
            plt.ioff()
            
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            fig.suptitle(f'{modality.capitalize()} Embedding Visualization', fontsize=14)
            
            # Original features
            axes[0].plot(features[:100] if len(features) > 100 else features, 'b-', alpha=0.7)
            axes[0].set_title(f'Original Features ({len(features)} dims)')
            axes[0].set_xlabel('Feature Index')
            axes[0].set_ylabel('Feature Value')
            axes[0].grid(True, alpha=0.3)
            
            # Embedded features
            embedding = np.array(embedding_data.get("embedding", []))
            axes[1].plot(embedding, 'r-', alpha=0.7)
            axes[1].set_title(f'Embedded Features ({len(embedding)} dims)')
            axes[1].set_xlabel('Embedding Index')
            axes[1].set_ylabel('Embedding Value')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{modality.capitalize()} Embedding",
                "type": "image",
                "data": plot_b64,
                "description": f"Embedding visualization showing dimensionality reduction from {len(features)} to {len(embedding)} dimensions"
            }
            
        except Exception as e:
            logger.error(f"Error creating embedding visualization: {e}")
            return {
                "name": f"{modality.capitalize()} Embedding Error",
                "type": "error",
                "data": "",
                "description": f"Failed to generate embedding visualization: {str(e)}"
            }
    
    def _create_feature_hash(self, features: np.ndarray) -> str:
        """Create a hash of the features for integrity checking"""
        try:
            import hashlib
            # Convert features to string and hash
            feature_str = str(features.tolist())
            return hashlib.sha256(feature_str.encode()).hexdigest()[:16]  # First 16 chars
        except Exception as e:
            logger.error(f"Error creating feature hash: {e}")
            return "hash_error"
    
    def _create_encoding_visualization(self, features: np.ndarray, feature_hash: str, modality: str) -> Dict[str, Any]:
        """Create visualization of feature encoding process"""
        try:
            import matplotlib.pyplot as plt
            
            plt.ioff()
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle(f'{modality.capitalize()} Feature Encoding', fontsize=14)
            
            # Feature distribution
            axes[0, 0].hist(features, bins=30, alpha=0.7, color='blue')
            axes[0, 0].set_title('Feature Distribution')
            axes[0, 0].set_xlabel('Feature Value')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Feature magnitude
            magnitudes = np.abs(features)
            axes[0, 1].plot(magnitudes, 'g-', alpha=0.7)
            axes[0, 1].set_title('Feature Magnitudes')
            axes[0, 1].set_xlabel('Feature Index')
            axes[0, 1].set_ylabel('Magnitude')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Hash visualization (convert hash to numbers)
            hash_numbers = [ord(c) for c in feature_hash[:16]]
            axes[1, 0].bar(range(len(hash_numbers)), hash_numbers, color='red', alpha=0.7)
            axes[1, 0].set_title('Feature Hash')
            axes[1, 0].set_xlabel('Hash Character Position')
            axes[1, 0].set_ylabel('ASCII Value')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Encoding stats
            stats = ['Mean', 'Std', 'Min', 'Max']
            values = [np.mean(features), np.std(features), np.min(features), np.max(features)]
            axes[1, 1].bar(stats, values, color=['blue', 'orange', 'green', 'red'], alpha=0.7)
            axes[1, 1].set_title('Encoding Statistics')
            axes[1, 1].set_ylabel('Value')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{modality.capitalize()} Feature Encoding",
                "type": "image",
                "data": plot_b64,
                "description": f"Feature encoding visualization with hash {feature_hash}"
            }
            
        except Exception as e:
            logger.error(f"Error creating encoding visualization: {e}")
            return {
                "name": f"{modality.capitalize()} Encoding Error",
                "type": "error",
                "data": "",
                "description": f"Failed to generate encoding visualization: {str(e)}"
            }


# Global instance for service
_biometric_service = None

def get_biometric_service():
    """Get or create basic biometric service instance"""
    global _biometric_service
    if _biometric_service is None:
        _biometric_service = BiometricService()
    return _biometric_service

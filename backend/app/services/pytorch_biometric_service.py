import os
import io
import base64
import hashlib
import logging
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import skew, kurtosis
import cv2
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

logger = logging.getLogger(__name__)


class PyTorchBiometricService:
    """Advanced biometric verification using PyTorch deep learning models"""
    
    def __init__(self):
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        logger.info(f"Using device: {self.device}")
        
        # Load pre-trained ResNet model for feature extraction (optimized)
        self.feature_extractor = models.resnet50(pretrained=True)
        # Remove the final classification layer
        children = list(self.feature_extractor.children())[:-1]
        self.feature_extractor = nn.Sequential(*children)
        self.feature_extractor.to(self.device)
        self.feature_extractor.eval()
        
        # Enable optimizations for faster inference
        if self.device.type == 'cpu':
            # Optimize for CPU inference
            torch.set_num_threads(4)  # Use 4 threads for CPU processing
        
        # Use torch.jit.script for faster inference (if possible)
        try:
            # Create a dummy input to trace the model
            dummy_input = torch.randn(1, 3, 224, 224).to(self.device)
            self.feature_extractor = torch.jit.trace(self.feature_extractor, dummy_input)
            logger.info("Model optimized with TorchScript tracing")
        except Exception as e:
            logger.warning(f"Could not optimize model with TorchScript: {e}")
        
        # Define optimized image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BILINEAR),  # Faster interpolation
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        logger.info("PyTorch biometric service initialized successfully with optimizations")
    
    def extract_features(self, image: np.ndarray, biometric_type: str = "face") -> np.ndarray:
        """Extract deep learning features from image using ResNet (optimized for speed)"""
        try:
            # Convert numpy array to PIL Image (optimized conversion)
            if isinstance(image, np.ndarray):
                if image.dtype != np.uint8:
                    image = (image * 255).astype(np.uint8)
                
                # Optimized image format handling
                if len(image.shape) == 3 and image.shape[2] == 3:
                    pil_image = Image.fromarray(image, mode='RGB')
                elif len(image.shape) == 2:
                    pil_image = Image.fromarray(image, mode='L').convert('RGB')
                else:
                    pil_image = Image.fromarray(image).convert('RGB')
            else:
                pil_image = image.convert('RGB')
            
            # Apply biometric-type-specific preprocessing (optimized)
            if biometric_type == "face":
                # Optimized face preprocessing - faster cropping
                width, height = pil_image.size
                
                # Simple center crop for face focus (faster than detection)
                crop_size = min(width, height) * 0.8
                left = int((width - crop_size) / 2)
                top = int((height - crop_size) / 3)
                right = int(left + crop_size)
                bottom = int(top + crop_size)
                
                # Clamp to image bounds
                left = max(0, min(left, width))
                top = max(0, min(top, height))
                right = max(left, min(right, width))
                bottom = max(top, min(bottom, height))
                
                if right > left and bottom > top:
                    pil_image = pil_image.crop((left, top, right, bottom))
                    logger.info(f"Face cropped from {width}x{height} to {pil_image.size[0]}x{pil_image.size[1]}")
                
            elif biometric_type in ["fingerprint", "palmprint"]:
                # Enhanced contrast for better feature extraction (optimized)
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Contrast(pil_image)
                pil_image = enhancer.enhance(1.5)  # Increase contrast by 50%
                logger.info(f"Enhanced {biometric_type} contrast for better feature extraction")
            
            # Transform image for model input and extract features (optimized pipeline)
            with torch.no_grad():  # Disable gradient computation for faster inference
                input_tensor = self.transform(pil_image).unsqueeze(0).to(self.device)
                
                # Extract features with optimized inference
                features = self.feature_extractor(input_tensor)
                features = features.view(features.size(0), -1)  # Flatten
                features_np = features.cpu().numpy().flatten()
                
                # Normalize features for better comparison
                features_np = features_np / (np.linalg.norm(features_np) + 1e-8)
                
                logger.info(f"Extracted {len(features_np)}-dimensional features for {biometric_type} using ResNet50")
                return features_np
            
        except Exception as e:
            logger.error(f"Error extracting features for {biometric_type}: {e}")
            raise
    
    def _calculate_quality_metrics(self, image: np.ndarray, biometric_type: str) -> Dict[str, float]:
        """Calculate quality metrics for biometric image"""
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = np.mean(image, axis=2)
            else:
                gray = image
                
            # Basic quality metrics
            contrast = np.std(gray)
            sharpness = np.var(np.gradient(gray))
            brightness = np.mean(gray)
            
            # Normalize to 0-100 scale
            contrast_score = min(100, (contrast / 128) * 100)
            sharpness_score = min(100, (sharpness / 1000) * 100)
            brightness_score = 100 - abs(brightness - 128) / 128 * 100
            
            return {
                "contrast": contrast_score,
                "sharpness": sharpness_score, 
                "brightness": brightness_score,
                "overall": (contrast_score + sharpness_score + brightness_score) / 3
            }
            
        except Exception as e:
            logger.error(f"Error calculating quality metrics: {e}")
            return {"contrast": 0, "sharpness": 0, "brightness": 0, "overall": 0}
    
    def _detect_edges(self, image: np.ndarray) -> np.ndarray:
        """Simple edge detection using gradients"""
        try:
            if len(image.shape) == 3:
                gray = np.mean(image, axis=2)
            else:
                gray = image.astype(float)
                
            # Simple Sobel-like edge detection
            dx = np.gradient(gray, axis=1)
            dy = np.gradient(gray, axis=0)
            edges = np.sqrt(dx**2 + dy**2)
            
            # Normalize to 0-255
            edges = ((edges - edges.min()) / (edges.max() - edges.min() + 1e-8) * 255).astype(np.uint8)
            
            return edges
            
        except Exception as e:
            logger.error(f"Error detecting edges: {e}")
            return np.zeros_like(image)
    
    def _create_classification_visualization(self, image: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create classification visualization showing biometric analysis"""
        try:
            plt.ioff()  # Turn off interactive mode
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{biometric_type.capitalize()} PyTorch Analysis', fontsize=16)
            
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
            quality_scores = self._calculate_quality_metrics(gray_img, biometric_type)
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
                "name": f"{biometric_type.capitalize()} PyTorch Classification",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"PyTorch ResNet50 classification analysis for {biometric_type}"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "Classification", biometric_type)
    
    def _create_extraction_visualization(self, image: np.ndarray, features: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create feature extraction visualization"""
        try:
            plt.ioff()
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{biometric_type.capitalize()} Feature Extraction (ResNet50)', fontsize=16)
            
            # 1. Original image with feature points
            if len(image.shape) == 3:
                display_img = image
            else:
                display_img = np.stack([image] * 3, axis=-1)
                
            axes[0, 0].imshow(display_img)
            axes[0, 0].set_title('Image with Feature Regions')
            axes[0, 0].axis('off')
            
            # Add some feature point markers
            h, w = image.shape[:2]
            for i in range(0, min(20, len(features)), len(features)//20):
                y = int((i % 10) * h / 10)
                x = int((i // 10) * w / 2)
                axes[0, 0].plot(x, y, 'ro', markersize=3)
            
            # 2. Feature vector plot (first 100 features)
            feature_subset = features[:100]
            axes[0, 1].plot(feature_subset, 'b-', linewidth=1)
            axes[0, 1].set_title('Feature Vector (First 100)')
            axes[0, 1].set_xlabel('Feature Index')
            axes[0, 1].set_ylabel('Feature Value')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Feature importance heatmap (reshape first 64 features)
            heatmap_features = features[:64].reshape(8, 8)
            im = axes[1, 0].imshow(heatmap_features, cmap='viridis', aspect='auto')
            axes[1, 0].set_title('Feature Importance Heatmap')
            plt.colorbar(im, ax=axes[1, 0])
            
            # 4. Feature statistics
            stats = {
                'Mean': np.mean(features),
                'Std': np.std(features),
                'Skew': skew(features),
                'Kurt': kurtosis(features)
            }
            
            stat_names = list(stats.keys())
            stat_values = list(stats.values())
            
            axes[1, 1].bar(stat_names, stat_values, color=['purple', 'orange', 'green', 'red'])
            axes[1, 1].set_title('Feature Statistics')
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
                "name": f"{biometric_type.capitalize()} Feature Extraction",
                "type": "image",
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"ResNet50 feature extraction analysis showing {len(features)} features"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "Extraction", biometric_type)
    
    def _verify_biometric_core(self, stored_features: Any, input_features: Any,
                         threshold: float = None) -> Tuple[bool, float]:
        """
        Verify biometric using adaptive thresholds for real-world variations
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
            
            # Validate dimensions
            if stored.shape != input_feat.shape:
                logger.error(
                    f"Feature dimension mismatch: stored={stored.shape}, "
                    f"input={input_feat.shape}"
                )
                return False, 0.0
            
            # Calculate multiple similarity metrics for robust verification
            # 1. Cosine similarity (main metric)
            norm_stored = np.linalg.norm(stored)
            norm_input = np.linalg.norm(input_feat)
            cosine_sim = np.dot(stored, input_feat) / (norm_stored * norm_input)
            
            # 2. Pearson correlation
            correlation = np.corrcoef(stored, input_feat)[0, 1]
            if np.isnan(correlation):
                correlation = 0.0
            
            # 3. Normalized dot product
            normalized_dot = np.dot(stored / norm_stored, input_feat / norm_input)
            
            # Use adaptive thresholds based on feature statistics
            feature_variance = np.var(stored)
            
            if threshold is None:
                # Use more lenient thresholds for face recognition due to clothing/lighting variations
                if feature_variance > 0.01:  # High variance features (more discriminative)
                    base_threshold = 0.65  # More lenient for faces
                else:  # Low variance features (typical for cropped faces)
                    base_threshold = 0.70  # Much more lenient for face recognition
            else:
                base_threshold = threshold
            
            # Multi-metric verification (more robust)
            cosine_pass = cosine_sim >= base_threshold
            correlation_pass = abs(correlation) >= (base_threshold - 0.05)
            dot_pass = normalized_dot >= (base_threshold - 0.05)
            
            # Require at least 2 out of 3 metrics to pass
            passed_count = sum([cosine_pass, correlation_pass, dot_pass])
            is_match = passed_count >= 2
            
            # For logging, use cosine similarity as primary score
            primary_score = cosine_sim
            
            logger.info("=== PYTORCH ADAPTIVE VERIFICATION ===")
            logger.info(f"  Cosine similarity: {cosine_sim:.6f} (threshold: {base_threshold}) {'✓' if cosine_pass else '✗'}")
            logger.info(f"  Correlation: {correlation:.6f} (threshold: {base_threshold-0.05:.2f}) {'✓' if correlation_pass else '✗'}")
            logger.info(f"  Normalized dot: {normalized_dot:.6f} (threshold: {base_threshold-0.05:.2f}) {'✓' if dot_pass else '✗'}")
            logger.info(f"  Feature variance: {feature_variance:.6f}")
            logger.info(f"  Passed metrics: {passed_count}/3 (2+ required)")
            result_str = 'AUTHENTICATED' if is_match else 'REJECTED'
            logger.info(f"  FINAL RESULT: {result_str}")
            logger.info("=====================================")
            
            return is_match, primary_score
            
        except Exception as e:
            logger.error(f"Error in biometric verification: {e}")
            return False, 0.0
    
    def process_biometric_registration(self, image_data: bytes, 
                                     biometric_type: str) -> Dict[str, Any]:
        """Process biometric data for registration with detailed analysis"""
        try:
            start_time = datetime.now()
            
            # Decode image
            image = Image.open(io.BytesIO(image_data))
            original_size = image.size
            image_array = np.array(image)
            
            # Store original image
            original_image_b64 = base64.b64encode(image_data).decode()
            
            # Processing steps tracking
            processing_steps = []
            visualizations = []
            
            # Step 1: Image preprocessing
            processing_steps.append({
                "step": 1,
                "name": "Image Preprocessing",
                "description": f"Loaded {biometric_type} image with size {original_size}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Step 2: PyTorch feature extraction
            processing_steps.append({
                "step": 2,
                "name": "PyTorch ResNet50 Processing",
                "description": f"Applying ResNet50 feature extraction for {biometric_type}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Extract features using appropriate preprocessing for biometric type
            features = self.extract_features(image_array, biometric_type=biometric_type)
            
            processing_steps.append({
                "step": 3,
                "name": "Feature Extraction Complete",
                "description": f"Extracted {len(features)} features using ResNet50",
                "timestamp": datetime.now().isoformat()
            })
            
            # Step 4: Enhanced visualization generation
            processing_steps.append({
                "step": 4,
                "name": "Comprehensive Visualization Generation",
                "description": "Creating detailed analysis visualizations for all processing steps",
                "timestamp": datetime.now().isoformat()
            })
            
            # Generate comprehensive visualizations
            visualizations = []
            
            # 1. Original image visualization
            original_viz = self._create_original_image_visualization(image_array, biometric_type)
            visualizations.append(original_viz)
            
            # 2. Preprocessing steps visualization
            preprocess_viz = self._create_preprocessing_visualization(image_array, image_array, biometric_type)
            visualizations.append(preprocess_viz)
            
            # 3. Edge detection visualization
            edge_viz = self._create_edge_detection_visualization(image_array, biometric_type)
            visualizations.append(edge_viz)
            
            # 4. Region of interest visualization
            roi_viz = self._create_roi_visualization(image_array, biometric_type)
            visualizations.append(roi_viz)
            
            # 5. Feature extraction visualization
            extract_viz = self._create_extraction_visualization(image_array, features, biometric_type)
            visualizations.append(extract_viz)
            
            # 6. Classification analysis visualization
            class_viz = self._create_classification_visualization(image_array, biometric_type)
            visualizations.append(class_viz)
            
            # 7. Quality assessment visualization
            quality_viz = self._create_quality_assessment_visualization(image_array, biometric_type)
            visualizations.append(quality_viz)
            
            # 8. Feature distribution visualization
            feature_dist_viz = self._create_feature_distribution_visualization(features, biometric_type)
            visualizations.append(feature_dist_viz)
            
            # Step 5: Quality assessment
            quality_metrics = self._calculate_quality_metrics(image_array, biometric_type)
            
            processing_steps.append({
                "step": 5,
                "name": "Quality Assessment",
                "description": f"Quality score: {quality_metrics['overall']:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
            
            # Create hash
            feature_hash = hashlib.sha256(features.tobytes()).hexdigest()
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return {
                "success": True,
                "features": features.tolist(),
                "hash": feature_hash,
                "feature_length": len(features),
                "biometric_type": biometric_type,
                "detailed_analysis": {
                    "processing_mode": "pytorch_unified", 
                    "model": "ResNet50",
                    "feature_dimensions": len(features),
                    "processing_steps": len(processing_steps),
                    "visualizations": len(visualizations),
                    "quality_score": quality_metrics["overall"],
                    "processing_time": f"{processing_time:.2f}s",
                    "image_info": {
                        "original_size": original_size,
                        "original_image": original_image_b64
                    },
                    "steps": processing_steps,
                    "generated_visualizations": visualizations,
                    "quality_metrics": quality_metrics
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing biometric registration: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_biometric_login(self, image_data: bytes, 
                              biometric_type: str) -> Dict[str, Any]:
        """Process biometric data for login"""
        try:
            # Decode image
            if isinstance(image_data, str):
                # If it's base64 string, decode it
                image_bytes = base64.b64decode(image_data)
            else:
                image_bytes = image_data
                
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Extract features using appropriate preprocessing for biometric type
            features = self.extract_features(image_array, biometric_type=biometric_type)
            
            return {
                "success": True,
                "features": features.tolist(),
                "feature_length": len(features),
                "biometric_type": biometric_type
            }
            
        except Exception as e:
            logger.error(f"Error processing biometric login: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _create_original_image_visualization(self, image: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create visualization of the original image with analysis annotations"""
        try:
            plt.ioff()  # Turn off interactive mode
            
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            fig.suptitle(f'{biometric_type.capitalize()} - Original Image Analysis', fontsize=16)
            
            # Ensure image is in correct format
            if len(image.shape) == 3:
                display_img = image
                gray_img = np.mean(image, axis=2).astype(np.uint8)
            else:
                gray_img = image.astype(np.uint8)
                display_img = np.stack([gray_img] * 3, axis=-1)
            
            # Original image
            axes[0].imshow(display_img)
            axes[0].set_title('Original Image')
            axes[0].axis('off')
            
            # Image with analysis grid
            axes[1].imshow(display_img)
            axes[1].set_title('Analysis Grid Overlay')
            axes[1].axis('off')
            
            # Add analysis grid
            h, w = gray_img.shape
            for i in range(0, h, h//8):
                axes[1].axhline(y=i, color='red', alpha=0.3, linewidth=1)
            for i in range(0, w, w//8):
                axes[1].axvline(x=i, color='red', alpha=0.3, linewidth=1)
            
            plt.tight_layout()
            
            # Save to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{biometric_type.capitalize()} - Original Image",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"Original {biometric_type} image with analysis grid overlay"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "Original Image", biometric_type)
    
    def _create_preprocessing_visualization(self, original: np.ndarray, processed: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create visualization showing preprocessing steps"""
        try:
            plt.ioff()
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle(f'{biometric_type.capitalize()} - Preprocessing Steps', fontsize=16)
            
            # Convert to grayscale if needed
            if len(original.shape) == 3:
                orig_gray = np.mean(original, axis=2).astype(np.uint8)
            else:
                orig_gray = original.astype(np.uint8)
                
            if len(processed.shape) == 3:
                proc_gray = np.mean(processed, axis=2).astype(np.uint8)
            else:
                proc_gray = processed.astype(np.uint8)
            
            # 1. Original
            axes[0, 0].imshow(orig_gray, cmap='gray')
            axes[0, 0].set_title('Original')
            axes[0, 0].axis('off')
            
            # 2. Histogram equalization
            equalized = cv2.equalizeHist(orig_gray)
            axes[0, 1].imshow(equalized, cmap='gray')
            axes[0, 1].set_title('Histogram Equalized')
            axes[0, 1].axis('off')
            
            # 3. Gaussian blur
            blurred = cv2.GaussianBlur(orig_gray, (5, 5), 0)
            axes[0, 2].imshow(blurred, cmap='gray')
            axes[0, 2].set_title('Gaussian Blur')
            axes[0, 2].axis('off')
            
            # 4. Enhanced contrast
            enhanced = cv2.convertScaleAbs(orig_gray, alpha=1.2, beta=30)
            axes[1, 0].imshow(enhanced, cmap='gray')
            axes[1, 0].set_title('Enhanced Contrast')
            axes[1, 0].axis('off')
            
            # 5. Final processed
            axes[1, 1].imshow(proc_gray, cmap='gray')
            axes[1, 1].set_title('Final Processed')
            axes[1, 1].axis('off')
            
            # 6. Difference visualization
            diff = cv2.absdiff(orig_gray, proc_gray)
            axes[1, 2].imshow(diff, cmap='hot')
            axes[1, 2].set_title('Processing Difference')
            axes[1, 2].axis('off')
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{biometric_type.capitalize()} - Preprocessing Steps",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"Step-by-step preprocessing visualization for {biometric_type}"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "Preprocessing", biometric_type)
    
    def _create_edge_detection_visualization(self, image: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create edge detection visualization"""
        try:
            plt.ioff()
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{biometric_type.capitalize()} - Edge Detection Analysis', fontsize=16)
            
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = np.mean(image, axis=2).astype(np.uint8)
            else:
                gray = image.astype(np.uint8)
            
            # 1. Original
            axes[0, 0].imshow(gray, cmap='gray')
            axes[0, 0].set_title('Original Image')
            axes[0, 0].axis('off')
            
            # 2. Canny edge detection
            edges = cv2.Canny(gray, 50, 150)
            axes[0, 1].imshow(edges, cmap='gray')
            axes[0, 1].set_title('Canny Edge Detection')
            axes[0, 1].axis('off')
            
            # 3. Sobel edge detection
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel = np.sqrt(sobelx**2 + sobely**2)
            axes[1, 0].imshow(sobel, cmap='gray')
            axes[1, 0].set_title('Sobel Edge Detection')
            axes[1, 0].axis('off')
            
            # 4. Laplacian edge detection
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            axes[1, 1].imshow(np.abs(laplacian), cmap='gray')
            axes[1, 1].set_title('Laplacian Edge Detection')
            axes[1, 1].axis('off')
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{biometric_type.capitalize()} - Edge Detection",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"Edge detection analysis using multiple algorithms for {biometric_type}"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "Edge Detection", biometric_type)
    
    def _create_roi_visualization(self, image: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create region of interest visualization"""
        try:
            plt.ioff()
            
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            fig.suptitle(f'{biometric_type.capitalize()} - Region of Interest Analysis', fontsize=16)
            
            # Convert to display format
            if len(image.shape) == 3:
                display_img = image
                gray = np.mean(image, axis=2).astype(np.uint8)
            else:
                gray = image.astype(np.uint8)
                display_img = np.stack([gray] * 3, axis=-1)
            
            h, w = gray.shape
            
            # 1. Original with ROI overlay
            axes[0].imshow(display_img)
            axes[0].set_title('Original with ROI')
            axes[0].axis('off')
            
            # Add ROI rectangles based on biometric type
            if biometric_type == 'face':
                # Face regions: eyes, nose, mouth
                roi_rects = [
                    (w*0.2, h*0.2, w*0.6, h*0.3),  # Eye region
                    (w*0.35, h*0.4, w*0.3, h*0.2),  # Nose region
                    (w*0.3, h*0.65, w*0.4, h*0.2),  # Mouth region
                ]
            elif biometric_type == 'fingerprint':
                # Fingerprint regions: center, ridges
                roi_rects = [
                    (w*0.3, h*0.3, w*0.4, h*0.4),  # Center core
                    (w*0.1, h*0.1, w*0.8, h*0.8),  # Full ridge area
                ]
            else:  # palmprint
                # Palm regions: major lines, texture areas
                roi_rects = [
                    (w*0.2, h*0.2, w*0.6, h*0.6),  # Main palm area
                    (w*0.1, h*0.4, w*0.8, h*0.2),  # Horizontal lines
                ]
            
            for rect in roi_rects:
                x, y, width, height = rect
                rect_patch = patches.Rectangle((x, y), width, height, 
                                             linewidth=2, edgecolor='red', facecolor='none', alpha=0.7)
                axes[0].add_patch(rect_patch)
            
            # 2. ROI mask
            mask = np.zeros_like(gray)
            for rect in roi_rects:
                x, y, width, height = [int(coord) for coord in rect]
                mask[y:y+height, x:x+width] = 255
            
            axes[1].imshow(mask, cmap='hot')
            axes[1].set_title('ROI Mask')
            axes[1].axis('off')
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{biometric_type.capitalize()} - Region of Interest",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"Region of interest analysis for {biometric_type} with key feature areas highlighted"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "ROI", biometric_type)
    
    def _create_quality_assessment_visualization(self, image: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create quality assessment visualization"""
        try:
            plt.ioff()
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle(f'{biometric_type.capitalize()} - Quality Assessment', fontsize=16)
            
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = np.mean(image, axis=2).astype(np.uint8)
            else:
                gray = image.astype(np.uint8)
            
            # 1. Original image
            axes[0, 0].imshow(gray, cmap='gray')
            axes[0, 0].set_title('Original Image')
            axes[0, 0].axis('off')
            
            # 2. Brightness analysis
            brightness = np.mean(gray)
            axes[0, 1].hist(gray.flatten(), bins=50, alpha=0.7, color='blue')
            axes[0, 1].axvline(brightness, color='red', linestyle='--', label=f'Mean: {brightness:.1f}')
            axes[0, 1].set_title('Brightness Distribution')
            axes[0, 1].legend()
            
            # 3. Contrast analysis
            contrast = np.std(gray)
            axes[0, 2].imshow(gray, cmap='gray')
            axes[0, 2].set_title(f'Contrast Score: {contrast:.1f}')
            axes[0, 2].axis('off')
            
            # 4. Sharpness (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            axes[1, 0].imshow(np.abs(laplacian), cmap='hot')
            axes[1, 0].set_title(f'Sharpness: {sharpness:.1f}')
            axes[1, 0].axis('off')
            
            # 5. Noise analysis (using high-pass filter)
            kernel = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])
            noise = cv2.filter2D(gray, -1, kernel)
            noise_level = np.std(noise)
            axes[1, 1].imshow(np.abs(noise), cmap='hot')
            axes[1, 1].set_title(f'Noise Level: {noise_level:.1f}')
            axes[1, 1].axis('off')
            
            # 6. Overall quality score
            quality_score = self._calculate_quality_metrics(image, biometric_type)
            overall_quality = quality_score['overall']
            
            # Create quality gauge
            angles = np.linspace(0, np.pi, 100)
            quality_color = 'green' if overall_quality > 70 else 'orange' if overall_quality > 40 else 'red'
            
            axes[1, 2].plot(angles, np.ones_like(angles), color='lightgray', linewidth=10)
            quality_angle = (overall_quality / 100) * np.pi
            quality_angles = angles[angles <= quality_angle]
            if len(quality_angles) > 0:
                axes[1, 2].plot(quality_angles, np.ones_like(quality_angles), color=quality_color, linewidth=10)
            
            axes[1, 2].set_xlim(0, np.pi)
            axes[1, 2].set_ylim(0.5, 1.5)
            axes[1, 2].set_title(f'Overall Quality: {overall_quality:.1f}%')
            axes[1, 2].axis('off')
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            plot_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "name": f"{biometric_type.capitalize()} - Quality Assessment",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"Comprehensive quality analysis including brightness, contrast, sharpness, and noise for {biometric_type}"
            }
            
        except Exception as e:
            return self._log_visualization_error(e, "Quality Assessment", biometric_type)
    
    def _create_feature_distribution_visualization(self, features: np.ndarray, biometric_type: str) -> Dict[str, Any]:
        """Create feature distribution visualization"""
        viz_name = "Feature Distribution"
        try:
            plt.ioff()
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{biometric_type.capitalize()} - Feature Distribution Analysis', fontsize=16)
            
            # 1. Feature histogram
            axes[0, 0].hist(features, bins=50, alpha=0.7, color='blue', edgecolor='black')
            axes[0, 0].set_title('Feature Value Distribution')
            axes[0, 0].set_xlabel('Feature Value')
            axes[0, 0].set_ylabel('Frequency')
            
            # 2. Feature statistics
            mean_val = np.mean(features)
            std_val = np.std(features)
            min_val = np.min(features)
            max_val = np.max(features)
            
            stats_text = f"""
Statistics:
Mean: {mean_val:.4f}
Std:  {std_val:.4f}
Min:  {min_val:.4f}
Max:  {max_val:.4f}
Range: {max_val - min_val:.4f}
            """.strip()
            
            axes[0, 1].text(0.1, 0.5, stats_text, transform=axes[0, 1].transAxes, 
                           fontsize=12, verticalalignment='center', fontfamily='monospace')
            axes[0, 1].set_title('Feature Statistics')
            axes[0, 1].axis('off')
            
            # 3. Feature variance visualization
            # Reshape features for visualization (show first 64 dimensions as 8x8 grid)
            viz_size = min(64, len(features))
            grid_size = int(np.sqrt(viz_size))
            if grid_size * grid_size < viz_size:
                grid_size += 1
            
            feature_grid = np.zeros((grid_size, grid_size))
            for i in range(min(viz_size, grid_size * grid_size)):
                row = i // grid_size
                col = i % grid_size
                if row < grid_size and col < grid_size:
                    feature_grid[row, col] = features[i]
            
            im = axes[1, 0].imshow(feature_grid, cmap='viridis', aspect='auto')
            axes[1, 0].set_title(f'Feature Map ({viz_size} features)')
            plt.colorbar(im, ax=axes[1, 0])
            
            # 4. Cumulative distribution
            sorted_features = np.sort(features)
            cumulative = np.arange(1, len(sorted_features) + 1) / len(sorted_features)
            axes[1, 1].plot(sorted_features, cumulative, 'b-', linewidth=2)
            axes[1, 1].set_title('Cumulative Distribution')
            axes[1, 1].set_xlabel('Feature Value')
            axes[1, 1].set_ylabel('Cumulative Probability')
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
                "id": f"feature_dist_{biometric_type}",
                "name": f"{biometric_type.capitalize()} - Feature Distribution",
                "type": "image", 
                "data": f"data:image/png;base64,{plot_b64}",
                "description": f"Statistical analysis and distribution of extracted features for {biometric_type}"
            } 
            
        except Exception as e:
            return self._log_visualization_error(e, viz_name, biometric_type)

    def _log_visualization_error(self, e: Exception, viz_name: str, biometric_type: str) -> Dict[str, Any]:
        """Log visualization errors with detailed traceback."""
        import traceback
        error_msg = f"Failed to generate '{viz_name}' visualization for {biometric_type}: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        return {
            "id": f"{viz_name.lower().replace(' ', '_')}_{biometric_type}_error",
            "name": f"{biometric_type.capitalize()} {viz_name} Error",
            "type": "error",
            "data": "",
            "description": error_msg
        }

    def process_face(self, image_data: bytes) -> Dict[str, Any]:
        """Process face image and extract features"""
        return self.process_biometric_registration(image_data, 'face')
    
    def process_fingerprint(self, image_data: bytes) -> Dict[str, Any]:
        """Process fingerprint image and extract features"""
        return self.process_biometric_registration(image_data, 'fingerprint')
    
    def process_palmprint(self, image_data: bytes) -> Dict[str, Any]:
        """Process palmprint image and extract features"""
        return self.process_biometric_registration(image_data, 'palmprint')
    
    def verify_biometric(self, biometric_type: str, stored_features: Any, input_features: Any) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Verify biometric with type-specific handling
        Returns (is_verified, confidence_score, verification_details)
        """
        try:
            # Use the core verification method
            is_verified, confidence_score = self._verify_biometric_core(stored_features, input_features)
            
            verification_details = {
                "biometric_type": biometric_type,
                "confidence_score": confidence_score,
                "threshold_used": "adaptive",
                "processing_mode": "pytorch_deep_learning"
            }
            
            logger.info(f"PyTorch {biometric_type} verification: {is_verified} (confidence: {confidence_score:.4f})")
            return is_verified, confidence_score, verification_details
            
        except Exception as e:
            logger.error(f"PyTorch verification error for {biometric_type}: {e}")
            return False, 0.0, {"error": str(e)}


# Global instance
pytorch_biometric_service = None


def get_pytorch_biometric_service():
    """Get or create PyTorch biometric service instance"""
    global pytorch_biometric_service
    if pytorch_biometric_service is None:
        pytorch_biometric_service = PyTorchBiometricService()
    return pytorch_biometric_service
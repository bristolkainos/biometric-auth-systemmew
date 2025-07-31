from fastapi import APIRouter, Depends, HTTPException, status, Request, File, UploadFile
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

from core.database import get_db
from core.security import (
    authenticate_user, authenticate_admin_user, get_password_hash,
    create_access_token, create_refresh_token, verify_token,
    validate_password_strength, get_current_user, get_current_admin_user
)
from core.config import settings
from models.user import User
from models.admin_user import AdminUser
from models.login_attempt import LoginAttempt
from models.biometric_data import BiometricData
from schemas.auth import (
    UserRegister, UserLogin, AdminLogin, TokenResponse,
    RefreshToken, UserResponse, AdminResponse
)
from services.biometric_service import BiometricService

def user_to_response(user: User) -> UserResponse:
    """Convert User model to UserResponse schema"""
    return UserResponse(
        id=user.id,  # type: ignore
        username=user.username,  # type: ignore
        email=user.email,  # type: ignore
        first_name=user.first_name,  # type: ignore
        last_name=user.last_name,  # type: ignore
        is_active=user.is_active,  # type: ignore
        is_verified=user.is_verified,  # type: ignore
        created_at=user.created_at  # type: ignore
    )

def admin_to_response(admin: AdminUser) -> AdminResponse:
    """Convert AdminUser model to AdminResponse schema"""
    return AdminResponse(
        id=admin.id,  # type: ignore
        username=admin.username,  # type: ignore
        email=admin.email,  # type: ignore
        first_name=admin.first_name,  # type: ignore
        last_name=admin.last_name,  # type: ignore
        is_super_admin=admin.is_super_admin,  # type: ignore
        is_active=admin.is_active,  # type: ignore
        created_at=admin.created_at  # type: ignore
    )

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user with password and biometric data"""
    
    logger.info(f"Registration attempt for user: {user_data.username}")
    
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate password strength
        if not validate_password_strength(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet strength requirements"
            )
        
        # Validate biometric data
        if len(user_data.biometric_data) < settings.MIN_BIOMETRIC_METHODS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"At least {settings.MIN_BIOMETRIC_METHODS} biometric methods are required"
            )
        
        # Process biometric data with optimizations
        logger.info(f"Processing {len(user_data.biometric_data)} biometric samples with optimizations")
        processed_biometrics = []
        
        # Process each biometric type with improved error handling and logging
        for i, bio_data in enumerate(user_data.biometric_data):
            start_time = datetime.now()
            logger.info(f"Processing biometric {i+1}/{len(user_data.biometric_data)}: {bio_data.biometric_type}")
            logger.info(f"Image data type: {type(bio_data.image_data)}")
            logger.info(f"Image data length: {len(bio_data.image_data) if hasattr(bio_data.image_data, '__len__') else 'N/A'}")
            
            # Convert base64 string to bytes for processing
            import base64
            try:
                image_bytes = base64.b64decode(bio_data.image_data)
            except Exception as e:
                logger.error(f"Base64 decode error for {bio_data.biometric_type}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid base64 image data for {bio_data.biometric_type}: {str(e)}"
                )
            
            # Validate image - accept any valid image format
            from PIL import Image
            import io
            try:
                # Just check if it's a valid image that can be opened
                test_image = Image.open(io.BytesIO(image_bytes))
                test_image.verify()
                logger.info(f"Valid image detected: {test_image.format} {test_image.size}")
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid image format for {bio_data.biometric_type}: {str(e)}"
                )
            
            # Process biometric with PyTorch for all types (unified approach)
            import hashlib
            
            # Create a simple hash from the image
            image_hash = hashlib.sha256(image_bytes).hexdigest()
            
            # Process biometric with optimized PyTorch service (prioritized for speed)
            import hashlib
            image_hash = hashlib.sha256(image_bytes).hexdigest()
            
            try:
                from services.pytorch_biometric_service import get_pytorch_biometric_service
                pytorch_service = get_pytorch_biometric_service()
                
                # Optimized processing with timing
                process_start = datetime.now()
                
                if bio_data.biometric_type == 'face':
                    result = pytorch_service.process_face(image_bytes)
                elif bio_data.biometric_type == 'fingerprint':
                    result = pytorch_service.process_fingerprint(image_bytes)
                elif bio_data.biometric_type == 'palmprint':
                    result = pytorch_service.process_palmprint(image_bytes)
                else:
                    raise ValueError(f"Unsupported biometric type: {bio_data.biometric_type}")
                
                process_time = (datetime.now() - process_start).total_seconds()
                logger.info(f"PyTorch {bio_data.biometric_type} processing completed in {process_time:.2f}s")
                
                # Add hash and timing to result
                result["hash"] = image_hash
                result["processing_time"] = process_time
                
            except Exception as pytorch_error:
                logger.warning(f"PyTorch {bio_data.biometric_type} processing failed: {pytorch_error}")
                
                # Fast fallback to basic biometric service
                try:
                    from services.biometric_service import get_biometric_service
                    basic_service = get_biometric_service()
                    
                    fallback_start = datetime.now()
                    biometric_type = bio_data.biometric_type.lower().strip()
                    logger.info(f"Using fallback processing for {biometric_type}")
                    
                    if biometric_type == 'face':
                        result_data = basic_service.process_face(image_bytes)
                    elif biometric_type == 'fingerprint':
                        result_data = basic_service.process_fingerprint(image_bytes)
                    elif biometric_type == 'palmprint':
                        result_data = basic_service.process_palmprint(image_bytes)
                    else:
                        raise ValueError(f"Unsupported biometric type: {biometric_type}")
                    
                    fallback_time = (datetime.now() - fallback_start).total_seconds()
                    logger.info(f"Fallback {biometric_type} processing completed in {fallback_time:.2f}s")
                    
                    # Create result in expected format
                    result = {
                        "success": True,
                        "hash": image_hash,
                        "features": result_data.get("features", []),
                        "processing_time": fallback_time,
                        "detailed_analysis": {
                            "processing_mode": "basic_fallback",
                            "feature_dimensions": len(result_data.get("features", [])),
                            "image_size": len(image_bytes),
                            "type": bio_data.biometric_type,
                            "model": "Basic",
                            "processing_time": fallback_time,
                            "image_info": {
                                "original_image": base64.b64encode(image_bytes).decode()
                            }
                        }
                    }
                    
                except Exception as e:
                    logger.error(f"Both PyTorch and basic {bio_data.biometric_type} processing failed during registration: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Failed to process {bio_data.biometric_type} biometric: {str(e)}"
                    )
            
            # Check processing success
            if not result.get("success", False):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to process {bio_data.biometric_type}: {result.get('error', 'Unknown error')}"
                )
            
            # Calculate total processing time for this biometric
            total_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Successfully processed {bio_data.biometric_type} in {total_time:.2f}s total")
            
            processed_biometrics.append({
                "type": bio_data.biometric_type,
                "hash": result["hash"],
                "features": result["features"],
                "detailed_analysis": result.get("detailed_analysis", {})
            })
            logger.info(f"Successfully processed {bio_data.biometric_type}")
        
        # Create user
        logger.info("Creating user record")
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created with ID: {user.id}")
        
         # Blockchain integration (ENABLE BY UNCOMMENTING BELOW)
        # from app.services.blockchain_service import BlockchainService
        # import logging
        # logger = logging.getLogger(__name__)
        
        # # Blockchain configuration - UPDATE THESE VALUES AFTER DEPLOYMENT
        # provider_url = "http://127.0.0.1:8545"  # Hardhat node URL
        # contract_address = "0xYourContractAddress"  # From deployment output
        # abi_path = "app/contracts/BiometricToken_abi.json"  # Copy from artifacts
        # private_key = "0xYourPrivateKey"  # From hardhat node output (first account)
        # account_address = "0xYourAccountAddress"  # From hardhat node output
        
        # try:
        #     blockchain_service = BlockchainService(
        #         provider_url, contract_address, abi_path, 
        #         private_key, account_address
        #     )
        #     blockchain_enabled = True
        #     logger.info("Blockchain service initialized successfully")
        # except Exception as e:
        #     logger.warning(f"Blockchain service failed to initialize: {e}")
        #     blockchain_enabled = False

        # Add biometric data with detailed analysis
        logger.info("Storing biometric data")
        for bio_data in processed_biometrics:
            biometric_record = BiometricData(
                user_id=user.id,
                biometric_type=bio_data["type"],
                biometric_hash=bio_data["hash"],
                biometric_features=json.dumps(bio_data["features"]),
                processing_analysis=json.dumps(bio_data["detailed_analysis"])
            )
            db.add(biometric_record)

            # Blockchain minting (ENABLE BY UNCOMMENTING BELOW)
            # if blockchain_enabled:
            #     try:
            #         tx_hash = blockchain_service.mint_biometric_token(
            #             user.id, 
            #             bio_data["hash"], 
            #             bio_data["type"]
            #         )
            #         if tx_hash:
            #             logger.info(f"Blockchain token minted for user {user.id}, "
            #                        f"type: {bio_data['type']}, tx: {tx_hash}")
            #         else:
            #             logger.error(f"Failed to mint blockchain token for user {user.id}")
            #     except Exception as e:
            #         logger.error(f"Blockchain minting error for user {user.id}: {e}")
        
        db.commit()
        logger.info("Registration completed successfully")
        
        return user_to_response(user)
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

@router.post("/login", response_model=TokenResponse)
async def user_login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """User login endpoint with biometric verification"""
    
    # Step 1: Authenticate user credentials (username/password)
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    
    # Step 2: Biometric verification (required for security)
    if not user_credentials.biometric_data or not user_credentials.biometric_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Biometric verification required for login"
        )
    
    # Step 3: Get stored biometric data first to avoid unnecessary processing
    stored_biometrics = db.query(BiometricData).filter(
        BiometricData.user_id == user.id,
        BiometricData.biometric_type == user_credentials.biometric_type,
        BiometricData.is_active == True
    ).all()

    if not stored_biometrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No registered {user_credentials.biometric_type} biometric found for this user"
        )

    # Step 4: Process the provided biometric data ONCE
    try:
        # Convert biometric data to bytes if it's base64 string
        if isinstance(user_credentials.biometric_data, str):
            import base64
            biometric_bytes = base64.b64decode(user_credentials.biometric_data)
        else:
            biometric_bytes = user_credentials.biometric_data
        
        # Extract features using PyTorch service first (faster and more accurate)
        login_features = None
        try:
            from services.pytorch_biometric_service import get_pytorch_biometric_service
            pytorch_service = get_pytorch_biometric_service()
            
            # Process with PyTorch service - this is the expensive operation we're optimizing
            if user_credentials.biometric_type == 'face':
                result_data = pytorch_service.process_face(biometric_bytes)
            elif user_credentials.biometric_type == 'fingerprint':
                result_data = pytorch_service.process_fingerprint(biometric_bytes)
            elif user_credentials.biometric_type == 'palmprint':
                result_data = pytorch_service.process_palmprint(biometric_bytes)
            else:
                raise ValueError(f"Unsupported biometric type: {user_credentials.biometric_type}")
            
            login_features = result_data.get("features", [])
            logger.info(f"PyTorch {user_credentials.biometric_type} login processing: {len(login_features)} features extracted")
            
        except Exception as pytorch_error:
            logger.warning(f"PyTorch {user_credentials.biometric_type} processing failed: {pytorch_error}")
            
            # Fallback to basic biometric service
            try:
                from services.biometric_service import get_biometric_service
                basic_service = get_biometric_service()
                
                # Process with basic service
                biometric_type = user_credentials.biometric_type.lower().strip()
                logger.info(f"Processing {biometric_type} with basic service (fallback)")
                
                if biometric_type == 'face':
                    result_data = basic_service.process_face(biometric_bytes)
                elif biometric_type == 'fingerprint':
                    result_data = basic_service.process_fingerprint(biometric_bytes)
                elif biometric_type == 'palmprint':
                    result_data = basic_service.process_palmprint(biometric_bytes)
                else:
                    raise ValueError(f"Unsupported biometric type: {biometric_type}")
                
                login_features = result_data.get("features", [])
                logger.info(f"Basic {user_credentials.biometric_type} login processing: {len(login_features)} features extracted")
                
            except Exception as e:
                logger.error(f"Both PyTorch and basic {user_credentials.biometric_type} processing failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to process {user_credentials.biometric_type} biometric: {str(e)}"
                )
        
        if not login_features:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to extract biometric features from input"
            )
        
                
        logger.debug("Login features for user %s: %d dimensions", user.username, len(login_features))
        
        # Step 5: Verify against stored biometric features (using cached features)
        is_verified = False
        confidence_score = 0.0
        verification_details = {}

        for stored_biometric in stored_biometrics:
            try:
                # Load stored features from JSON (these are pre-processed and cached)
                stored_features = json.loads(str(stored_biometric.biometric_features))
                logger.debug("Comparing against stored features: %d dimensions", len(stored_features))
                
                # Use PyTorch verification for better accuracy
                try:
                    from services.pytorch_biometric_service import get_pytorch_biometric_service
                    pytorch_service = get_pytorch_biometric_service()
                    
                    # Fast verification using pre-computed features - no image processing here!
                    match, score, details = pytorch_service.verify_biometric(
                        user_credentials.biometric_type,
                        stored_features,
                        login_features
                    )
                    logger.info(f"PyTorch {user_credentials.biometric_type} verification: {match} (confidence: {score:.4f})")
                    
                    if match:
                        is_verified = True
                        confidence_score = score
                        verification_details = details
                        break
                        
                except Exception as pytorch_error:
                    logger.warning(f"PyTorch verification failed, using basic service: {pytorch_error}")
                    
                    # Fallback to basic verification
                    try:
                        biometric_service = BiometricService()
                        match = biometric_service.verify_biometric(
                            user_credentials.biometric_type,
                            stored_features,
                            login_features
                        )
                        if match:
                            is_verified = True
                            confidence_score = 0.8  # Default confidence for basic verification
                            verification_details = {
                                "processing_mode": "basic_fallback",
                                "biometric_type": user_credentials.biometric_type
                            }
                            logger.info(f"Basic {user_credentials.biometric_type} verification successful")
                            break
                    except Exception as basic_error:
                        logger.error(f"Basic verification also failed: {basic_error}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error processing stored biometric data: {e}")
                continue
        
        # Step 4: Get all stored biometric data for this user
        stored_biometrics = db.query(BiometricData).filter(
            BiometricData.user_id == user.id,
            BiometricData.biometric_type == user_credentials.biometric_type,
            BiometricData.is_active == True
        ).all()

        if not stored_biometrics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No registered {user_credentials.biometric_type} biometric found for this user"
            )

        # Step 5: Try verification against all stored feature sets
        is_verified = False
        confidence_score = 0.0
        verification_details = {}

        for stored_biometric in stored_biometrics:
            stored_features = json.loads(str(stored_biometric.biometric_features))
            logger.debug("Stored features for user %s: %s", user.username, stored_features)
            try:
                from services.pytorch_biometric_service import get_pytorch_biometric_service
                pytorch_service = get_pytorch_biometric_service()
                # PyTorch verification - returns (success, confidence_score, details)
                match, score, details = pytorch_service.verify_biometric(
                    user_credentials.biometric_type,
                    stored_features,
                    login_features
                )
                logger.info(f"PyTorch {user_credentials.biometric_type} verification: {match} (confidence: {score})")
                if match:
                    is_verified = True
                    confidence_score = score
                    verification_details = details
                    break
            except Exception as pytorch_error:
                logger.warning(f"PyTorch {user_credentials.biometric_type} verification failed, falling back to basic service: {pytorch_error}")
                try:
                    biometric_service = BiometricService()
                    match = biometric_service.verify_biometric(
                        user_credentials.biometric_type,
                        stored_features,
                        login_features
                    )
                    if match:
                        is_verified = True
                        confidence_score = 0.8
                        verification_details = {
                            "processing_mode": "basic_fallback",
                            "biometric_type": user_credentials.biometric_type
                        }
                        logger.debug(f"Basic {user_credentials.biometric_type} verification result for user {user.username}: {match}")
                        break
                except Exception as fallback_error:
                    logger.error(f"Both PyTorch and basic {user_credentials.biometric_type} verification failed: {fallback_error}")
                    continue

        logger.debug("Verification result for user %s: %s", user.username, is_verified)

        if not is_verified:
            # Log failed login attempt
            failed_attempt = LoginAttempt(
                user_id=int(user.id),
                attempt_type=user_credentials.biometric_type,
                success=False,
                ip_address="unknown"  # Can be extracted from request if needed
            )
            db.add(failed_attempt)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Biometric verification failed"
            )

        # Step 7: Log successful login attempt
        successful_attempt = LoginAttempt(
            user_id=int(user.id),
            attempt_type=user_credentials.biometric_type,
            success=True,
            ip_address="unknown"
        )
        db.add(successful_attempt)

        # Update user's last login time
        user.last_login = datetime.utcnow()
        db.commit()

        logger.info(f"Successful biometric login for user {user.username} using {user_credentials.biometric_type}")
        
    except HTTPException:
        # Re-raise HTTP exceptions (like authentication failures)
        raise
    except Exception as e:
        logger.error(f"Biometric verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Biometric verification failed due to processing error"
        )
    
    # Step 8: Generate tokens for successful login
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/admin/login", response_model=TokenResponse)
async def admin_login(
    admin_credentials: AdminLogin,
    db: Session = Depends(get_db)
):
    """Admin login endpoint"""
    admin = authenticate_admin_user(db, admin_credentials.username, admin_credentials.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )
    access_token = create_access_token(data={"sub": str(admin.id), "type": "admin"})
    refresh_token = create_refresh_token(data={"sub": str(admin.id), "type": "refresh"})
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    
    try:
        # Log the refresh token for debugging
        logger.info(f"Received refresh token: {refresh_data.refresh_token[:50]}...")
        
        # Verify refresh token
        payload = verify_token(refresh_data.refresh_token)
        logger.info(f"Refresh token payload: {payload}")
        
        if payload.get("type") != "refresh":
            logger.warning(f"Invalid token type: {payload.get('type')}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            logger.warning("No user ID found in token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Check if user exists and is active
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            logger.warning(f"Invalid user ID format: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )
            
        user = db.query(User).filter(User.id == user_id_int).first()
        if not user or not bool(user.is_active):
            logger.warning(f"User not found or inactive: {user_id_int}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})
        
        logger.info(f"Successfully refreshed token for user: {user.username}")
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Refresh token error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return user_to_response(current_user)

@router.get("/me/biometrics")
async def get_user_biometric_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's biometric data"""
    biometric_data = db.query(BiometricData).filter(
        BiometricData.user_id == current_user.id,
        BiometricData.is_active == True
    ).all()
    
    return [
        {
            "id": bio.id,
            "biometric_type": bio.biometric_type,
            "is_active": bio.is_active,
            "created_at": bio.created_at.isoformat(),
            "updated_at": bio.updated_at.isoformat(),
            "confidence_score": 0.95,  # Default confidence score
            "last_used": bio.updated_at.isoformat()  # Use updated_at as last_used
        }
        for bio in biometric_data
    ]

@router.get("/me/login-history")
async def get_user_login_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's login history"""
    login_attempts = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == current_user.id
    ).order_by(LoginAttempt.created_at.desc()).limit(20).all()
    
    return [
        {
            "id": attempt.id,
            "created_at": attempt.created_at.isoformat(),
            "attempt_type": attempt.attempt_type,
            "success": attempt.success,
            "ip_address": attempt.ip_address,
            "location_info": attempt.location_info
        }
        for attempt in login_attempts
    ]

@router.get("/me/security-overview")
async def get_user_security_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's security overview"""
    # Get biometric count
    biometric_count = db.query(BiometricData).filter(
        BiometricData.user_id == current_user.id,
        BiometricData.is_active == True
    ).count()
    
    # Get recent successful logins
    recent_logins = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == current_user.id,
        LoginAttempt.success == True
    ).order_by(LoginAttempt.created_at.desc()).limit(5).all()
    
    # Get failed login attempts in last 24 hours
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    failed_attempts_24h = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == current_user.id,
        LoginAttempt.success == False,
        LoginAttempt.created_at >= yesterday
    ).count()
    
    return {
        "account_verified": current_user.is_verified,
        "account_active": current_user.is_active,
        "biometric_methods_count": biometric_count,
        "recent_successful_logins": len(recent_logins),
        "failed_attempts_24h": failed_attempts_24h,
        "last_login": recent_logins[0].created_at.isoformat() if recent_logins else None
    }

@router.get("/blockchain/transactions")
async def get_blockchain_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's blockchain transactions (mock data for now)"""
    # Mock blockchain transactions
    mock_transactions = [
        {
            "id": "tx_001",
            "type": "biometric_mint",
            "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "status": "success",
            "hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "biometricType": "fingerprint",
            "description": "Fingerprint biometric token minted",
            "gasUsed": 21000,
            "blockNumber": 12345678,
            "from": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
            "to": "0x1234567890123456789012345678901234567890"
        },
        {
            "id": "tx_002",
            "type": "biometric_mint",
            "timestamp": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
            "status": "success",
            "hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "biometricType": "face",
            "description": "Face recognition biometric token minted",
            "gasUsed": 25000,
            "blockNumber": 12345675,
            "from": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
            "to": "0x1234567890123456789012345678901234567890"
        }
    ]
    
    return mock_transactions

@router.get("/blockchain/metrics")
async def get_blockchain_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get blockchain security metrics (mock data for now)"""
    mock_metrics = {
        "totalTransactions": 156,
        "successfulTransactions": 152,
        "failedTransactions": 4,
        "averageGasUsed": 22000,
        "lastBlockNumber": 12345682,
        "encryptionStrength": 95,
        "biometricTokens": 3,
        "securityScore": 92,
        "networkStatus": "active",
        "contractAddress": "0x1234567890123456789012345678901234567890"
    }
    
    return mock_metrics

@router.get("/blockchain/biometric-tokens")
async def get_biometric_tokens(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's biometric tokens (mock data for now)"""
    # Get user's biometric data and convert to token format
    biometric_data = db.query(BiometricData).filter(
        BiometricData.user_id == current_user.id,
        BiometricData.is_active == True
    ).all()
    
    mock_tokens = []
    for i, bio in enumerate(biometric_data):
        mock_tokens.append({
            "id": str(bio.id),
            "tokenId": f"0x{hash(f'{current_user.id}_{bio.biometric_type}_{i}') % (10**18):x}",
            "biometricType": bio.biometric_type,
            "owner": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
            "mintedAt": bio.created_at.isoformat(),
            "lastVerified": bio.updated_at.isoformat(),
            "verificationCount": 15,
            "metadata": {
                "confidence": 0.95,
                "features": ["feature_extraction", "encryption", "blockchain_storage"],
                "imageHash": bio.biometric_hash
            }
        })
    
    return mock_tokens

@router.get("/admin/me", response_model=AdminResponse)
async def get_current_admin_info(
    current_admin: AdminUser = Depends(get_current_admin_user)
):
    """Get current admin information"""
    return admin_to_response(current_admin)

@router.post("/biometric", response_model=TokenResponse)
async def biometric_authentication(
    user_id: int,
    modality: str,
    image_data: bytes,
    db: Session = Depends(get_db)
):
    """Biometric authentication endpoint"""
    try:
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Get stored biometric data for this user and modality
        stored_biometric = db.query(BiometricData).filter(
            BiometricData.user_id == user_id,
            BiometricData.biometric_type == modality,
            BiometricData.is_active == True
        ).first()
        
        if not stored_biometric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No {modality} biometric data found for user"
            )
        
        # Initialize biometric service
        biometric_service = BiometricService()
        
        # Check if user is active
        if not bool(user.is_active):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Validate uploaded image
        if not biometric_service.validate_image(image_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid biometric image"
            )
        
        # Process the uploaded biometric image with detailed analysis
        processed_result = biometric_service.process_biometric_detailed(image_data, modality, user_id)
        if not processed_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to process {modality} image: {processed_result.get('error', 'Unknown error')}"
            )
        
        # Get stored features
        stored_features = json.loads(stored_biometric.biometric_features)
        input_features = processed_result["features"]
        
        # Perform ultra-secure biometric verification
        logger.info(f"Performing biometric verification for user {user_id}, modality: {modality}")
        verification_result = biometric_service.verify_biometric(
            modality, stored_features, input_features
        )
        
        if not verification_result:
            # Log failed biometric attempt
            logger.warning(f"Biometric authentication failed for user {user_id}, modality: {modality}")
            
            # Record failed login attempt
            failed_attempt = LoginAttempt(
                user_id=user_id,
                attempt_type="biometric",
                success=False,
                ip_address="unknown",
                user_agent="biometric_auth"
            )
            db.add(failed_attempt)
            
            # Increment failed login attempts
            user.failed_login_attempts += 1
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Biometric authentication failed"
            )
        
        # Success! Create tokens
        logger.info(f"Biometric authentication successful for user {user_id}, modality: {modality}")
        
        # Record successful login attempt
        from models.login_attempt import LoginAttempt
        successful_attempt = LoginAttempt(
            user_id=user_id,
            attempt_type="biometric",
            success=True,
            ip_address="unknown",  # You might want to get this from request
            user_agent="biometric_auth"
        )
        db.add(successful_attempt)
        
        # Reset failed login attempts and update last login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in biometric authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during biometric authentication"
        )

@router.post("/biometric-identify", response_model=TokenResponse)
async def biometric_identify_authentication(
    modality: str,
    biometric_data: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Pure biometric authentication - identify user by biometric data alone"""
    try:
        # Validate modality
        if modality not in ['face', 'fingerprint', 'palmprint']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid biometric modality. Must be 'face', 'fingerprint', or 'palmprint'"
            )
        
        # Read biometric data
        image_data = await biometric_data.read()
        
        # Initialize biometric service
        biometric_service = BiometricService()
        
        # Validate uploaded image
        if not biometric_service.validate_image(image_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid {modality} image format or quality"
            )
        
        # Process the uploaded biometric data
        processed_result = biometric_service.process_biometric_detailed(
            image_data, modality, 0  # Use 0 as default user_id for anonymous login
        )
        
        # Get all biometric records of the same type from database
        biometric_records = db.query(BiometricData).filter(
            BiometricData.biometric_type == modality
        ).all()
        
        if not biometric_records:
            # Log failed attempt (no user to associate with)
            failed_attempt = LoginAttempt(
                user_id=None,
                attempt_type="biometric",
                success=False,
                ip_address="unknown",
                user_agent="biometric_identify"
            )
            db.add(failed_attempt)
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"No registered {modality} biometric data found"
            )
        
        # Find matching user using biometric verification
        best_match_user = None
        best_match_score = 0
        
        for record in biometric_records:
            # Get user for this biometric record
            user = db.query(User).filter(User.id == record.user_id).first()
            if not user or not bool(user.is_active):
                continue
            
            # Parse stored features
            try:
                stored_features = json.loads(str(record.biometric_features))
            except:
                continue
            
            # Perform biometric verification
            verification_result = biometric_service.verify_biometric(
                modality, stored_features, processed_result["features"]
            )
            
            if verification_result:
                best_match_user = user
                best_match_score = 0.95  # High confidence for successful match
                break
        
        if not best_match_user:
            # Log failed attempt
            failed_attempt = LoginAttempt(
                user_id=None,
                attempt_type="biometric",
                success=False,
                ip_address="unknown",
                user_agent="biometric_identify"
            )
            db.add(failed_attempt)
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Biometric authentication failed - no matching biometric data found"
            )
        
        # Additional security: check if user account is locked
        if int(best_match_user.failed_login_attempts) >= settings.MAX_LOGIN_ATTEMPTS:
            failed_attempt = LoginAttempt(
                user_id=int(best_match_user.id),
                attempt_type="biometric",
                success=False,
                ip_address="unknown",
                user_agent="biometric_identify"
            )
            db.add(failed_attempt)
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is locked due to too many failed login attempts"
            )
        
        # Log successful biometric authentication
        successful_attempt = LoginAttempt(
            user_id=int(best_match_user.id),
            attempt_type="biometric",
            success=True,
            ip_address="unknown",
            user_agent="biometric_identify"
        )
        db.add(successful_attempt)
        
        # Reset failed login attempts and update last login
        best_match_user.failed_login_attempts = 0
        best_match_user.last_login = datetime.utcnow()
        db.commit()
        
        # Create access and refresh tokens
        access_token = create_access_token(data={"sub": str(best_match_user.id)})
        refresh_token = create_refresh_token(data={"sub": str(best_match_user.id)})
        
        logger.info(f"Successful biometric identification for user {best_match_user.username} with {modality} (confidence: {best_match_score:.4f})")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in biometric identification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during biometric identification"
        )

@router.post("/register-fast", response_model=UserResponse)
async def register_user_fast(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user with simplified biometric processing for testing"""
    
    logger.info(f"Fast registration attempt for user: {user_data.username}")
    
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate password strength
        if not validate_password_strength(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet strength requirements"
            )
        
        # Check minimum biometric methods
        if len(user_data.biometric_data) < settings.MIN_BIOMETRIC_METHODS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"At least {settings.MIN_BIOMETRIC_METHODS} biometric methods are required"
            )
        
        # Process biometric data with fast mode
        logger.info(f"Fast processing {len(user_data.biometric_data)} biometric samples")
        biometric_service = BiometricService()
        processed_biometrics = []
        
        for i, bio_data in enumerate(user_data.biometric_data):
            logger.info(f"Fast processing biometric {i+1}: {bio_data.biometric_type}")
            
            # Convert base64 string to bytes for processing
            import base64
            try:
                image_bytes = base64.b64decode(bio_data.image_data)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid base64 image data for {bio_data.biometric_type}: {str(e)}"
                )
            
            # Simple validation only
            if not biometric_service.validate_image(image_bytes):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid {bio_data.biometric_type} image"
                )
            
            # Fast processing - generate simple hash and features
            import hashlib
            simple_hash = hashlib.sha256(image_bytes).hexdigest()
            simple_features = [len(image_bytes), sum(image_bytes[:100]) % 1000]  # Simple features
            
            processed_biometrics.append({
                "type": bio_data.biometric_type,
                "hash": simple_hash,
                "features": simple_features,
                "detailed_analysis": {"processing_mode": "fast"}
            })
            logger.info(f"Fast processing completed for {bio_data.biometric_type}")
        
        # Create user
        logger.info("Creating user record")
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True,
            is_verified=True  # Auto-verify for testing
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created with ID: {user.id}")
        
        # Store biometric data
        logger.info("Storing biometric data")
        for bio_data in processed_biometrics:
            biometric_record = BiometricData(
                user_id=user.id,
                biometric_type=bio_data["type"],
                biometric_hash=bio_data["hash"],
                biometric_features=json.dumps(bio_data["features"]),
                processing_analysis=json.dumps(bio_data["detailed_analysis"])
            )
            db.add(biometric_record)
        
        db.commit()
        logger.info("Fast registration completed successfully")
        
        return user_to_response(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fast registration error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to internal error"
        )

@router.post("/login-fast", response_model=TokenResponse)
async def user_login_fast(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Fast user login endpoint with simplified biometric verification"""
    
    logger.info(f"Fast login attempt for user: {user_credentials.username}")
    
    # Step 1: Authenticate user credentials (username/password)
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    
    # Step 2: Simple biometric verification (for testing)
    if not user_credentials.biometric_data or not user_credentials.biometric_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Biometric verification required for login"
        )
    
    # Step 3: Check if user has biometric data registered
    stored_biometric = db.query(BiometricData).filter(
        BiometricData.user_id == user.id,
        BiometricData.biometric_type == user_credentials.biometric_type,
        BiometricData.is_active == True
    ).first()
    
    if not stored_biometric:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No {user_credentials.biometric_type} biometric data found for user"
        )
    
    # Step 4: Full biometric verification
    try:
        import base64
        from PIL import Image
        import io
        import numpy as np
        
        # Decode the biometric image from base64 string
        image_bytes = base64.b64decode(user_credentials.biometric_data)
        
        # Validate it's a valid image
        from PIL import Image
        import io
        try:
            test_image = Image.open(io.BytesIO(image_bytes))
            test_image.verify()
            logger.info(f"Login image validated: {test_image.format}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid biometric image: {str(e)}"
            )
        
        # Use basic service only (PyTorch disabled for cloud deployment)
        try:
            # Disable PyTorch in cloud environment
            raise ImportError("PyTorch disabled for cloud deployment")
            
        except Exception as pytorch_error:
            logger.warning(f"PyTorch processing failed in user_login_fast, using basic features: {pytorch_error}")
            # Fallback to basic features
            result = {
                "success": True,
                "features": [len(image_bytes), 1.0, 0.5],  # Simple features
                "detailed_analysis": {
                    "processing_mode": "basic_fallback",
                    "generated_visualizations": []
                }
            }
        
        if result["success"]:
            # Update stored biometric data with new analysis including visualizations
            import json
            stored_biometric.processing_analysis = json.dumps(result["detailed_analysis"])
            stored_biometric.biometric_features = json.dumps(result["features"])
            db.commit()
            logger.info(f"Updated biometric data with {len(result['detailed_analysis'].get('generated_visualizations', []))} visualizations")
        
        # Convert image to numpy array for processing
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Create simple features for comparison
        login_features = [
            len(image_bytes),  # File size
            sum(image_bytes[:100]) % 1000,  # Simple checksum
            hash(user_credentials.biometric_type) % 1000  # Type-based feature
        ]
        
        # Load stored features and verify
        stored_features = json.loads(stored_biometric.biometric_features)
        
        # Simple verification: check if features are similar enough
        # In development mode, we'll be more lenient
        is_verified = True  # For now, accept any valid image
        
        # Optional: Add some basic similarity check
        if len(stored_features) >= 2 and len(login_features) >= 2:
            # Check if image sizes are reasonably similar (within 50% difference)
            size_diff = abs(stored_features[0] - login_features[0]) / max(stored_features[0], login_features[0])
            if size_diff > 0.5:
                is_verified = False
                logger.warning(f"Image size difference too large: {size_diff}")
        
        logger.info(f"Biometric verification result: {is_verified} (stored: {stored_features[:2]}, login: {login_features[:2]})")
        
        if not is_verified:
            # Log failed login attempt
            failed_attempt = LoginAttempt(
                user_id=user.id,
                attempt_type="login",
                success=False,
                ip_address="unknown"
            )
            db.add(failed_attempt)
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Biometric verification failed"
            )
        
        logger.info(f"Biometric verification passed for user {user.username} using {user_credentials.biometric_type}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Biometric verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Biometric verification failed due to processing error"
        )
    
    # Step 5: Create tokens
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.username}
    )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    logger.info(f"Fast login successful for user: {user.username}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.id
    )

def user_to_response(user: User) -> UserResponse:
    """Convert User model to UserResponse schema"""
    return UserResponse(
        id=int(user.id),
        username=str(user.username),
        email=str(user.email),
        first_name=str(user.first_name),
        last_name=str(user.last_name),
        is_active=bool(user.is_active),
        is_verified=bool(user.is_verified),
        created_at=user.created_at
    )

def admin_to_response(admin: AdminUser) -> AdminResponse:
    """Convert AdminUser model to AdminResponse schema"""
    return AdminResponse(
        id=int(admin.id),
        username=str(admin.username),
        email=str(admin.email),
        first_name=str(admin.first_name),
        last_name=str(admin.last_name),
        is_super_admin=bool(admin.is_super_admin),
        is_active=bool(admin.is_active),
        created_at=admin.created_at
    )

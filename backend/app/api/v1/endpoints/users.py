from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.admin_user import AdminUser
from app.models.biometric_data import BiometricData
from app.models.login_attempt import LoginAttempt
from app.schemas.auth import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )

@router.get("/biometric-data")
async def get_user_biometric_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's biometric data information (without sensitive features)"""
    biometric_data = db.query(BiometricData).filter(
        BiometricData.user_id == current_user.id,
        BiometricData.is_active == True
    ).all()
    
    return {
        "user_id": current_user.id,
        "biometric_methods": [
            {
                "id": data.id,
                "type": data.biometric_type,
                "created_at": data.created_at,
                "updated_at": data.updated_at
            }
            for data in biometric_data
        ],
        "total_methods": len(biometric_data)
    }

@router.delete("/biometric-data/{biometric_id}")
async def delete_biometric_data(
    biometric_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific biometric data entry"""
    biometric_data = db.query(BiometricData).filter(
        BiometricData.id == biometric_id,
        BiometricData.user_id == current_user.id
    ).first()
    
    if not biometric_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Biometric data not found"
        )
    
    # Check if user would have enough biometric methods after deletion
    remaining_methods = db.query(BiometricData).filter(
        BiometricData.user_id == current_user.id,
        BiometricData.is_active == True,
        BiometricData.id != biometric_id
    ).count()
    
    from app.core.config import settings
    if remaining_methods < settings.MIN_BIOMETRIC_METHODS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete biometric data. Minimum {settings.MIN_BIOMETRIC_METHODS} methods required"
        )
    
    # Soft delete
    biometric_data.is_active = False
    db.commit()
    
    return {
        "message": "Biometric data deleted successfully"
    }


@router.get("/dashboard")
async def get_my_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's dashboard data"""
    try:
        # Get user's biometric data
        biometric_data = db.query(BiometricData).filter(
            BiometricData.user_id == current_user.id,
            BiometricData.is_active == True
        ).all()
        
        # Get user's login attempts (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        login_attempts = db.query(LoginAttempt).filter(
            LoginAttempt.user_id == current_user.id,
            LoginAttempt.created_at >= thirty_days_ago
        ).order_by(LoginAttempt.created_at.desc()).limit(50).all()
        
        # Calculate basic analytics
        total_logins = len(login_attempts)
        successful_logins = len([la for la in login_attempts if la.success])
        failed_logins = total_logins - successful_logins
        success_rate = (successful_logins / total_logins * 100) if total_logins > 0 else 0
        
        # Group biometric methods
        biometric_methods = []
        for data in biometric_data:
            try:
                analysis = json.loads(data.processing_analysis) if data.processing_analysis else {}
                biometric_methods.append({
                    "id": data.id,
                    "type": data.biometric_type,
                    "created_at": data.created_at.isoformat(),
                    "updated_at": data.updated_at.isoformat(),
                    "quality_score": analysis.get("quality_score", 0)
                })
            except (json.JSONDecodeError, Exception):
                biometric_methods.append({
                    "id": data.id,
                    "type": data.biometric_type,
                    "created_at": data.created_at.isoformat(),
                    "updated_at": data.updated_at.isoformat(),
                    "quality_score": 0
                })
        
        # Recent login history
        login_history = []
        for attempt in login_attempts[:10]:  # Last 10 attempts
            login_history.append({
                "id": attempt.id,
                "attempt_type": attempt.attempt_type,
                "success": attempt.success,
                "created_at": attempt.created_at.isoformat(),
                "ip_address": attempt.ip_address or "unknown"
            })
        
        return {
            "user_details": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "first_name": current_user.first_name,
                "last_name": current_user.last_name,
                "is_active": current_user.is_active,
                "is_verified": current_user.is_verified,
                "created_at": current_user.created_at.isoformat(),
                "last_login": current_user.last_login.isoformat() if current_user.last_login else None
            },
            "biometric_data": biometric_methods,
            "login_history": login_history,
            "analytics": {
                "total_logins": total_logins,
                "successful_logins": successful_logins,
                "failed_logins": failed_logins,
                "success_rate": round(success_rate, 2),
                "total_biometric_methods": len(biometric_methods)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard data for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard data"
        )

@router.put("/profile")
async def update_user_profile(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    if first_name:
        current_user.first_name = first_name
    if last_name:
        current_user.last_name = last_name
    if email:
        # Check if email already exists
        existing_user = db.query(User).filter(
            User.email == email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = email
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )


@router.get("/{user_id}/dashboard")
async def get_user_dashboard_data(
    user_id: int,
    current_admin: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive user dashboard data for admin view"""
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get biometric data
    biometric_data = db.query(BiometricData).filter(
        BiometricData.user_id == user_id,
        BiometricData.is_active
    ).all()
    
    # Get login attempts (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    login_attempts = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == user_id,
        LoginAttempt.created_at >= thirty_days_ago
    ).order_by(LoginAttempt.created_at.desc()).all()
    
    # Calculate analytics
    total_logins = len(login_attempts)
    successful_logins = len([la for la in login_attempts if la.success])
    failed_logins = total_logins - successful_logins
    success_rate = (successful_logins / total_logins * 100) if total_logins > 0 else 0
    
    # Group by biometric method
    biometric_usage = {}
    for data in biometric_data:
        method = data.biometric_type
        if method not in biometric_usage:
            biometric_usage[method] = 0
        biometric_usage[method] += 1
    
    # Create login trend data (last 7 days)
    login_trend = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_logins = len([
            la for la in login_attempts 
            if day_start <= la.created_at < day_end
        ])
        
        login_trend.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "logins": day_logins
        })
    
    login_trend.reverse()  # Oldest to newest
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "last_login": user.last_login
        },
        "analytics": {
            "totalLogins": total_logins,
            "successfulLogins": successful_logins,
            "failedLogins": failed_logins,
            "successRate": round(success_rate, 1),
            "biometricUsage": biometric_usage,
            "loginTrend": login_trend
        },
        "login_attempts": [
            {
                "id": la.id,
                "success": la.success,
                "biometric_type": la.attempt_type,  # Changed from la.biometric_type to la.attempt_type
                "created_at": la.created_at,
                "ip_address": la.ip_address
            }
            for la in login_attempts[:20]  # Last 20 attempts
        ],
        "biometric_methods": [
            {
                "id": data.id,
                "type": data.biometric_type,
                "created_at": data.created_at,
                "updated_at": data.updated_at
            }
            for data in biometric_data
        ]
    }

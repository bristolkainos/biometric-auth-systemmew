from fastapi import APIRouter
from .endpoints import auth, users, admin, biometric

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(biometric.router, prefix="/biometric", tags=["biometric"]) 

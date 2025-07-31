from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        
    def _clean_old_requests(self, client_ip: str):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]
    
    async def __call__(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        # Initialize request list for new IP
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Clean old requests
        self._clean_old_requests(client_ip)
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again in a minute."
                }
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Continue processing the request
        return None

class BiometricRateLimiter:
    def __init__(self, max_attempts: int = 3, lockout_time: int = 300):
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time  # in seconds
        self.failed_attempts: Dict[str, list] = {}
        self.lockouts: Dict[str, float] = {}
    
    def _clean_old_attempts(self, client_ip: str):
        """Remove attempts older than lockout time"""
        current_time = time.time()
        self.failed_attempts[client_ip] = [
            attempt_time for attempt_time in self.failed_attempts[client_ip]
            if current_time - attempt_time < self.lockout_time
        ]
    
    async def __call__(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        # Check if IP is locked out
        if client_ip in self.lockouts:
            if current_time - self.lockouts[client_ip] < self.lockout_time:
                remaining_time = int(self.lockout_time - (current_time - self.lockouts[client_ip]))
                logger.warning(f"Blocked biometric attempt from locked out IP: {client_ip}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Too many failed attempts. Please try again in {remaining_time} seconds."
                    }
                )
            else:
                # Lockout expired
                del self.lockouts[client_ip]
                if client_ip in self.failed_attempts:
                    del self.failed_attempts[client_ip]
        
        # Initialize attempts list for new IP
        if client_ip not in self.failed_attempts:
            self.failed_attempts[client_ip] = []
        
        # Clean old attempts
        self._clean_old_attempts(client_ip)
        
        # Check attempts count
        if len(self.failed_attempts[client_ip]) >= self.max_attempts:
            self.lockouts[client_ip] = current_time
            logger.warning(f"IP locked out due to too many failed attempts: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Too many failed attempts. Please try again in {self.lockout_time} seconds."
                }
            )
        
        return None
    
    def record_failure(self, client_ip: str):
        """Record a failed biometric authentication attempt"""
        if client_ip not in self.failed_attempts:
            self.failed_attempts[client_ip] = []
        self.failed_attempts[client_ip].append(time.time())
    
    def record_success(self, client_ip: str):
        """Clear failed attempts on successful authentication"""
        if client_ip in self.failed_attempts:
            del self.failed_attempts[client_ip]
        if client_ip in self.lockouts:
            del self.lockouts[client_ip]

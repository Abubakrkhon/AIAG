"""
Rate Limiting Middleware
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_history = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Skip rate limiting for certain paths
        skip_paths = ["/health", "/", "/docs", "/redoc"]
        if any(request.url.path.startswith(p) for p in skip_paths):
            return await call_next(request)
        
        # Clean old entries
        current_time = time.time()
        minute_ago = current_time - 60
        
        self.request_history[client_ip] = [
            t for t in self.request_history[client_ip] 
            if t > minute_ago
        ]
        
        # Check rate limit
        if len(self.request_history[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Record this request
        self.request_history[client_ip].append(current_time)
        
        return await call_next(request)

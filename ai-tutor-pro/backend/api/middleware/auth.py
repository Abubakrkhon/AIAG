"""
Authentication Middleware
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    """Simple authentication middleware (placeholder)"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for certain paths
        skip_paths = ["/health", "/", "/docs", "/redoc", "/openapi.json"]
        
        if any(request.url.path.startswith(p) for p in skip_paths):
            return await call_next(request)
        
        # Get token from header
        token = request.headers.get("Authorization", "")
        
        # For now, just pass through (implement real auth later)
        # if not token.startswith("Bearer "):
        #     raise HTTPException(status_code=401, detail="Unauthorized")
        
        return await call_next(request)

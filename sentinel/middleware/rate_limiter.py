"""
VASTU ONE - Sentinel Rate Limiter
===================================
Simple in-memory rate limiter.
Blocks IPs that exceed request threshold.
"""
from __future__ import annotations
import time
from collections import defaultdict
from threading import Lock

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate limiter.
    
    Limits:
    - Auth endpoints: 10 requests / minute (brute force protection)
    - General API: 100 requests / minute
    """
    
    def __init__(self, app, auth_limit: int = 10, general_limit: int = 100, window_sec: int = 60):
        super().__init__(app)
        self.auth_limit = auth_limit
        self.general_limit = general_limit
        self.window_sec = window_sec
        # {(ip, bucket): [timestamps]}
        self._hits: dict[tuple[str, str], list[float]] = defaultdict(list)
        self._lock = Lock()
    
    def _get_ip(self, request: Request) -> str:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def _bucket(self, path: str) -> str:
        if path.startswith("/api/auth/login") or path.startswith("/api/auth/signup"):
            return "auth"
        return "general"
    
    def _check_limit(self, ip: str, bucket: str) -> tuple[bool, int]:
        """Returns (allowed, remaining)."""
        now = time.time()
        cutoff = now - self.window_sec
        key = (ip, bucket)
        
        with self._lock:
            # Clean old entries
            self._hits[key] = [t for t in self._hits[key] if t > cutoff]
            
            limit = self.auth_limit if bucket == "auth" else self.general_limit
            hits = len(self._hits[key])
            
            if hits >= limit:
                return False, 0
            
            self._hits[key].append(now)
            return True, limit - hits - 1
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Skip static, docs, health
        if path.startswith("/static/") or path in ("/health", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)
        
        ip = self._get_ip(request)
        bucket = self._bucket(path)
        
        allowed, remaining = self._check_limit(ip, bucket)
        
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Rate limit exceeded. Please try again later.",
                    "bucket": bucket,
                    "window_seconds": self.window_sec,
                },
                headers={
                    "Retry-After": str(self.window_sec),
                    "X-RateLimit-Limit": str(self.auth_limit if bucket == "auth" else self.general_limit),
                    "X-RateLimit-Remaining": "0",
                },
            )
        
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Bucket"] = bucket
        return response
"""
VASTU ONE - Sentinel Request Logger
=====================================
Logs every API request for security auditing.
Detects suspicious patterns and tracks anomalies.
"""
from __future__ import annotations
import time
import re
from datetime import datetime
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from database.base import AsyncSessionLocal
from database.models import AuditLog


# Patterns that trigger security alerts
SUSPICIOUS_PATTERNS = [
    r"(\.\./){2,}",              # Path traversal
    r"<script",                  # XSS attempt
    r"union\s+select",           # SQL injection
    r"exec\s*\(",                # Code injection
    r"\.\.%2f",                  # Encoded path traversal
    r"%00",                      # Null byte injection
    r"etc/passwd",               # LFI attempt
]

SUSPICIOUS_RE = re.compile("|".join(SUSPICIOUS_PATTERNS), re.IGNORECASE)


def is_suspicious(path: str, query: str = "") -> tuple[bool, str | None]:
    """Check if request path/query contains suspicious patterns."""
    target = f"{path}?{query}"
    match = SUSPICIOUS_RE.search(target)
    if match:
        return True, match.group(0)
    return False, None


class SentinelLoggerMiddleware(BaseHTTPMiddleware):
    """
    Logs every API request to the audit_logs table.
    Flags suspicious requests.
    """
    
    # Paths that we don't log (too noisy)
    SKIP_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip static + docs
        path = request.url.path
        if path in self.SKIP_PATHS or path.startswith("/static/"):
            return await call_next(request)
        
        start = time.time()
        
        # Check suspicious
        is_susp, pattern = is_suspicious(path, str(request.url.query))
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = round((time.time() - start) * 1000, 2)
        
        # Determine action name
        if is_susp:
            action = "SUSPICIOUS_REQUEST"
        elif response.status_code >= 500:
            action = "SERVER_ERROR"
        elif response.status_code >= 400:
            action = "CLIENT_ERROR"
        else:
            action = f"{request.method} {self._categorize(path)}"
        
        # Extract user_id from token if possible
        user_id = self._extract_user_id(request)
        
        # Log to DB asynchronously
        try:
            await self._log({
                "action": action,
                "entity_type": "http_request",
                "entity_id": None,
                "user_id": user_id,
                "ip_address": self._get_client_ip(request),
                "user_agent": request.headers.get("user-agent", "")[:500],
                "details": {
                    "method": request.method,
                    "path": path,
                    "query": str(request.url.query),
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                    "suspicious": is_susp,
                    "pattern_matched": pattern,
                },
            })
        except Exception:
            # Never fail the request due to logging
            pass
        
        # Add Sentinel headers to response
        response.headers["X-Sentinel-Logged"] = "true"
        if is_susp:
            response.headers["X-Sentinel-Suspicious"] = "true"
        
        return response
    
    def _categorize(self, path: str) -> str:
        """Categorize path for readable logs."""
        if path.startswith("/api/auth"):
            return "auth"
        if path.startswith("/api/clients"):
            return "clients"
        if path.startswith("/api/properties"):
            return "properties"
        if path.startswith("/api/reports"):
            return "reports"
        if path.startswith("/api/lms"):
            return "lms"
        return "other"
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP (behind proxy aware)."""
        # Check X-Forwarded-For first (proxy)
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()[:45]
        # Fallback to direct client
        return (request.client.host if request.client else "unknown")[:45]
    
    def _extract_user_id(self, request: Request) -> str | None:
        """Try to extract user_id from JWT without DB lookup."""
        try:
            auth = request.headers.get("authorization", "")
            if not auth.startswith("Bearer "):
                return None
            # Decode without verification (just to extract sub)
            from jose import jwt
            import os
            secret = os.getenv("JWT_SECRET_KEY", "change-me")
            algo = os.getenv("JWT_ALGORITHM", "HS256")
            payload = jwt.decode(auth[7:], secret, algorithms=[algo])
            return payload.get("sub")
        except Exception:
            return None
    
    async def _log(self, data: dict) -> None:
        """Write log to DB."""
        async with AsyncSessionLocal() as db:
            log = AuditLog(
                action=data["action"],
                entity_type=data.get("entity_type"),
                entity_id=data.get("entity_id"),
                user_id=data.get("user_id"),
                ip_address=data.get("ip_address"),
                user_agent=data.get("user_agent"),
                details=data.get("details", {}),
            )
            db.add(log)
            await db.commit()
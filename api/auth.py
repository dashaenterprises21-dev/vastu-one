"""
Vastu One - Authentication Core
JWT + Password hashing (bcrypt direct) + Session management
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User, Session as UserSession
from api.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_DAYS

# ═══ CONFIG ═══
SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = JWT_EXPIRE_DAYS
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_WINDOW_MIN = 15

security = HTTPBearer(auto_error=False)


# ═══ PASSWORD UTILS (bcrypt direct) ═══
def hash_password(password: str) -> str:
    """Hash password using bcrypt (with 72-byte truncation)"""
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        password_bytes = plain.encode("utf-8")[:72]
        hashed_bytes = hashed.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


# ═══ JWT UTILS ═══
def create_access_token(user_id: int, email: str, role: str) -> tuple:
    expires = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expires,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, expires


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# ═══ CURRENT USER ═══
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Check session is still valid
    session = db.query(UserSession).filter(
        UserSession.token == credentials.credentials,
        UserSession.is_active == True,
        UserSession.expires_at > datetime.now(timezone.utc),
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )

    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
"""
VASTU ONE - Auth Extended
==========================
Advanced auth logic: password reset, OTP, session management.
"""
from __future__ import annotations
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    User, PasswordResetToken, UserSession, OTPCode, AuditLog,
)


# ==========================================
# TOKEN / CODE GENERATION
# ==========================================
def generate_token(length: int = 32) -> str:
    """Generate a secure random URL-safe token."""
    return secrets.token_urlsafe(length)


def generate_otp(digits: int = 6) -> str:
    """Generate a numeric OTP."""
    return "".join(str(secrets.randbelow(10)) for _ in range(digits))


def hash_token(token: str) -> str:
    """SHA-256 hash a token for storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# ==========================================
# PASSWORD RESET
# ==========================================
async def create_password_reset_token(
    db: AsyncSession,
    user: User,
    expires_minutes: int = 30,
) -> str:
    """
    Create a password reset token for user.
    Returns the raw token (only shown once).
    """
    # Invalidate any existing unused tokens for this user
    await db.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .values(used_at=datetime.utcnow())
    )
    
    token = generate_token(32)
    token_hash = hash_token(token)
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    
    prt = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(prt)
    await db.commit()
    
    return token


async def verify_password_reset_token(
    db: AsyncSession,
    raw_token: str,
) -> Optional[User]:
    """Verify a reset token. Returns the user if valid."""
    token_hash = hash_token(raw_token)
    
    stmt = select(PasswordResetToken).where(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used_at.is_(None),
        PasswordResetToken.expires_at > datetime.utcnow(),
    )
    prt = (await db.execute(stmt)).scalar_one_or_none()
    if not prt:
        return None
    
    # Get user
    user = (await db.execute(select(User).where(User.id == prt.user_id))).scalar_one_or_none()
    return user


async def consume_password_reset_token(
    db: AsyncSession,
    raw_token: str,
) -> bool:
    """Mark a reset token as used."""
    token_hash = hash_token(raw_token)
    stmt = select(PasswordResetToken).where(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used_at.is_(None),
    )
    prt = (await db.execute(stmt)).scalar_one_or_none()
    if not prt:
        return False
    
    prt.used_at = datetime.utcnow()
    await db.commit()
    return True


# ==========================================
# OTP
# ==========================================
async def create_otp(
    db: AsyncSession,
    user: User,
    purpose: str,
    expires_minutes: int = 10,
) -> str:
    """Create an OTP code for user."""
    # Invalidate existing
    await db.execute(
        update(OTPCode)
        .where(
            OTPCode.user_id == user.id,
            OTPCode.purpose == purpose,
            OTPCode.used_at.is_(None),
        )
        .values(used_at=datetime.utcnow())
    )
    
    code = generate_otp(6)
    code_hash = hash_token(code)
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    
    otp = OTPCode(
        user_id=user.id,
        code_hash=code_hash,
        purpose=purpose,
        expires_at=expires_at,
    )
    db.add(otp)
    await db.commit()
    
    return code


async def verify_otp(
    db: AsyncSession,
    user: User,
    code: str,
    purpose: str,
) -> bool:
    """Verify an OTP code."""
    code_hash = hash_token(code)
    
    stmt = select(OTPCode).where(
        OTPCode.user_id == user.id,
        OTPCode.code_hash == code_hash,
        OTPCode.purpose == purpose,
        OTPCode.used_at.is_(None),
        OTPCode.expires_at > datetime.utcnow(),
    )
    otp = (await db.execute(stmt)).scalar_one_or_none()
    if not otp:
        return False
    
    otp.used_at = datetime.utcnow()
    await db.commit()
    return True


# ==========================================
# SESSIONS
# ==========================================
async def create_session(
    db: AsyncSession,
    user: User,
    refresh_token: str,
    ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    expires_days: int = 30,
) -> UserSession:
    """Create a session record for a refresh token."""
    session = UserSession(
        user_id=user.id,
        refresh_token_hash=hash_token(refresh_token),
        ip_address=ip,
        user_agent=(user_agent or "")[:500],
        device=_detect_device(user_agent or ""),
        expires_at=datetime.utcnow() + timedelta(days=expires_days),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def revoke_session(db: AsyncSession, session_id: str) -> bool:
    """Revoke a specific session."""
    session = (await db.execute(select(UserSession).where(UserSession.id == session_id))).scalar_one_or_none()
    if not session:
        return False
    
    session.is_active = False
    session.revoked_at = datetime.utcnow()
    await db.commit()
    return True


async def revoke_all_sessions(db: AsyncSession, user_id: str, except_id: Optional[str] = None) -> int:
    """Revoke all sessions for a user (optionally except one)."""
    stmt = update(UserSession).where(
        UserSession.user_id == user_id,
        UserSession.is_active == True,
    )
    if except_id:
        stmt = stmt.where(UserSession.id != except_id)
    stmt = stmt.values(is_active=False, revoked_at=datetime.utcnow())
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0


async def list_active_sessions(db: AsyncSession, user_id: str) -> list[UserSession]:
    """List active sessions for a user."""
    stmt = select(UserSession).where(
        UserSession.user_id == user_id,
        UserSession.is_active == True,
        UserSession.expires_at > datetime.utcnow(),
    ).order_by(UserSession.last_used_at.desc())
    return list((await db.execute(stmt)).scalars().all())


# ==========================================
# HELPERS
# ==========================================
def _detect_device(user_agent: str) -> str:
    """Detect device from user agent."""
    ua = user_agent.lower()
    if "iphone" in ua or "ipad" in ua:
        return "iOS"
    if "android" in ua:
        return "Android"
    if "windows" in ua:
        return "Windows"
    if "mac" in ua:
        return "Mac"
    if "linux" in ua:
        return "Linux"
    return "Unknown"


async def log_auth_event(
    db: AsyncSession,
    action: str,
    user_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict] = None,
) -> None:
    """Log auth-related audit event."""
    log = AuditLog(
        action=action,
        user_id=user_id,
        tenant_id=tenant_id,
        ip_address=ip,
        user_agent=(user_agent or "")[:500],
        details=details or {},
    )
    db.add(log)
    await db.commit()
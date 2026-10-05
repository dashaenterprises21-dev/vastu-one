"""
VASTU ONE - Auth Routes v2 (Extended)
=======================================
Forgot password, reset, OTP, sessions, change password.
"""
from __future__ import annotations
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import hash_password, verify_password, create_access_token, create_refresh_token
from api.auth_extended import (
    create_password_reset_token, verify_password_reset_token,
    consume_password_reset_token, create_otp, verify_otp,
    create_session, list_active_sessions, revoke_session, revoke_all_sessions,
    log_auth_event,
)
from api.dependencies import CurrentUser
from api.email_service import email_service
from database.base import get_db
from database.models import User


router = APIRouter(prefix="/api/auth", tags=["auth-v2"])


# ==========================================
# SCHEMAS
# ==========================================
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class SessionResponse(BaseModel):
    id: str
    device: str | None
    ip_address: str | None
    user_agent: str | None
    is_active: bool
    created_at: datetime
    last_used_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# FORGOT PASSWORD
# ==========================================
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    req: ForgotPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Send password reset email. Always returns 200 for security."""
    # Find user (don't reveal if exists)
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalars().first()
    
    if user and user.is_active:
        # Create token
        token = await create_password_reset_token(db, user)
        
        # Send email
        email_service.send_password_reset(
            to_email=user.email,
            full_name=user.full_name,
            reset_token=token,
        )
        
        # Log
        await log_auth_event(
            db, "PASSWORD_RESET_REQUESTED",
            user_id=user.id,
            tenant_id=user.tenant_id,
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent", ""),
        )
    
    # Always return success (don't leak email existence)
    return {
        "message": "If this email exists, a password reset link has been sent.",
    }


# ==========================================
# RESET PASSWORD (with token)
# ==========================================
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    req: ResetPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Reset password using a valid token."""
    # Verify token
    user = await verify_password_reset_token(db, req.token)
    if not user:
        raise HTTPException(400, "Invalid or expired reset token")
    
    # Update password
    user.password_hash = hash_password(req.new_password)
    await db.commit()
    
    # Consume token (single-use)
    await consume_password_reset_token(db, req.token)
    
    # Revoke all sessions (security)
    await revoke_all_sessions(db, user.id)
    
    # Send confirmation email
    email_service.send_password_changed(
        to_email=user.email,
        full_name=user.full_name,
    )
    
    # Log
    await log_auth_event(
        db, "PASSWORD_RESET_COMPLETED",
        user_id=user.id,
        tenant_id=user.tenant_id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", ""),
    )
    
    return {"message": "Password reset successfully. Please login with your new password."}


# ==========================================
# CHANGE PASSWORD (authenticated)
# ==========================================
@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    req: ChangePasswordRequest,
    request: Request,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Change password for authenticated user."""
    # Verify current password
    if not verify_password(req.current_password, current_user.password_hash):
        raise HTTPException(400, "Current password is incorrect")
    
    if req.current_password == req.new_password:
        raise HTTPException(400, "New password must be different from current")
    
    # Update
    current_user.password_hash = hash_password(req.new_password)
    await db.commit()
    
    # Send email
    email_service.send_password_changed(
        to_email=current_user.email,
        full_name=current_user.full_name,
    )
    
    # Log
    await log_auth_event(
        db, "PASSWORD_CHANGED",
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", ""),
    )
    
    return {"message": "Password changed successfully."}


# ==========================================
# SESSIONS — LIST
# ==========================================
@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """List all active sessions for current user."""
    sessions = await list_active_sessions(db, current_user.id)
    return sessions


# ==========================================
# SESSIONS — REVOKE ONE
# ==========================================
@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_one_session(
    session_id: str,
    request: Request,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Revoke a specific session."""
    # Verify session belongs to user
    sessions = await list_active_sessions(db, current_user.id)
    if not any(s.id == session_id for s in sessions):
        raise HTTPException(404, "Session not found")
    
    await revoke_session(db, session_id)
    
    await log_auth_event(
        db, "SESSION_REVOKED",
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        ip=request.client.host if request.client else None,
        details={"session_id": session_id},
    )
    
    return None


# ==========================================
# SESSIONS — REVOKE ALL
# ==========================================
@router.post("/sessions/revoke-all", status_code=status.HTTP_200_OK)
async def revoke_all(
    request: Request,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Revoke all sessions except current (requires re-login)."""
    count = await revoke_all_sessions(db, current_user.id)
    
    await log_auth_event(
        db, "ALL_SESSIONS_REVOKED",
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        ip=request.client.host if request.client else None,
        details={"count": count},
    )
    
    return {"message": f"Revoked {count} session(s).", "count": count}
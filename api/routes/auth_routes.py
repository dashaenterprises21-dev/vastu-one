"""
Vastu One - Authentication Routes
Signup, Login, Logout, Password Reset, Email/Phone verification
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import secrets

from database.db import get_db
from database.models import User, Session as UserSession, LoginAttempt, PasswordReset
from database.schemas import (
    UserSignup, UserLogin, UserResponse, TokenResponse,
    PasswordResetRequest, PasswordResetConfirm, MessageResponse
)
from api.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, MAX_LOGIN_ATTEMPTS, LOGIN_ATTEMPT_WINDOW_MIN,
    ACCESS_TOKEN_EXPIRE_DAYS
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ═══════════════════════════════════════
# SIGNUP
# ═══════════════════════════════════════
@router.post("/signup", response_model=TokenResponse)
def signup(data: UserSignup, request: Request, db: Session = Depends(get_db)):
    # Check email exists
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(status_code=400, detail="ईमेल पहले से registered है")

    # Check phone exists (if provided)
    if data.phone and db.query(User).filter(User.phone == data.phone).first():
        raise HTTPException(status_code=400, detail="फ़ोन नंबर पहले से registered है")

    # Create user
    user = User(
        name=data.name.strip(),
        email=data.email.lower(),
        phone=data.phone,
        password_hash=hash_password(data.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create token
    token, expires = create_access_token(user.id, user.email, user.role)

    # Create session
    session = UserSession(
        user_id=user.id,
        token=token,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", "")[:500],
        expires_at=expires,
    )
    db.add(session)
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_DAYS * 24 * 3600,
        user=UserResponse.model_validate(user),
    )


# ═══════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════
@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    email = data.email.lower()
    ip = request.client.host if request.client else "unknown"

    # Rate limit check
    window_start = datetime.now(timezone.utc) - timedelta(minutes=LOGIN_ATTEMPT_WINDOW_MIN)
    recent_fails = db.query(LoginAttempt).filter(
        LoginAttempt.email == email,
        LoginAttempt.success == False,
        LoginAttempt.attempted_at > window_start,
    ).count()

    if recent_fails >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail=f"बहुत ज़्यादा failed attempts। {LOGIN_ATTEMPT_WINDOW_MIN} मिनट बाद try करें।"
        )

    # Find user
    user = db.query(User).filter(User.email == email, User.is_active == True).first()

    # Log attempt
    attempt = LoginAttempt(email=email, ip_address=ip, success=False)

    if not user or not verify_password(data.password, user.password_hash):
        db.add(attempt)
        db.commit()
        raise HTTPException(status_code=401, detail="ईमेल या password गलत है")

    # Success — log
    attempt.success = True
    db.add(attempt)

    # Create token
    token, expires = create_access_token(user.id, user.email, user.role)

    # Create session
    session = UserSession(
        user_id=user.id,
        token=token,
        ip_address=ip,
        user_agent=request.headers.get("user-agent", "")[:500],
        expires_at=expires,
    )
    db.add(session)
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_DAYS * 24 * 3600,
        user=UserResponse.model_validate(user),
    )


# ═══════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════
@router.post("/logout", response_model=MessageResponse)
def logout(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    session = db.query(UserSession).filter(
        UserSession.token == token,
        UserSession.user_id == user.id,
    ).first()

    if session:
        session.is_active = False
        db.commit()

    return MessageResponse(message="Logout हो गया")


# ═══════════════════════════════════════
# ME (current user)
# ═══════════════════════════════════════
@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


# ═══════════════════════════════════════
# PASSWORD RESET
# ═══════════════════════════════════════
@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()

    # Always return success (security — don't reveal if email exists)
    if user:
        token = secrets.token_urlsafe(32)
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        db.add(reset)
        db.commit()
        # TODO: Send email with reset link

    return MessageResponse(
        message="अगर ईमेल registered है, reset link भेज दिया गया है"
    )


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    reset = db.query(PasswordReset).filter(
        PasswordReset.token == data.token,
        PasswordReset.used == False,
        PasswordReset.expires_at > datetime.now(timezone.utc),
    ).first()

    if not reset:
        raise HTTPException(status_code=400, detail="Token invalid या expired")

    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User नहीं मिला")

    user.password_hash = hash_password(data.new_password)
    reset.used = True
    db.commit()

    return MessageResponse(message="Password reset हो गया")
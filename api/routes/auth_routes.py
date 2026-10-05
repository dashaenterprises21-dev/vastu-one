"""
VASTU ONE - Auth Routes
========================
Signup, Login, Refresh, Me endpoints.
"""
from __future__ import annotations
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from api.dependencies import CurrentUser
from database.base import get_db
from database.models import Tenant, TenantPlan, User, UserRole


router = APIRouter(prefix="/api/auth", tags=["auth"])


# ==========================================
# SCHEMAS
# ==========================================
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: str | None = None
    role: UserRole = UserRole.CONSULTANT
    tenant_name: str | None = None
    tenant_slug: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    tenant_id: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    tenant_id: str
    is_active: bool
    is_verified: bool


# ==========================================
# SIGNUP
# ==========================================
@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(req: SignupRequest, db: AsyncSession = Depends(get_db)):
    """Create new user + optionally new tenant."""
    # Check existing email in the tenant
    if req.role == UserRole.CONSULTANT:
        if not req.tenant_slug:
            raise HTTPException(400, "tenant_slug required for consultants")
        
        slug = req.tenant_slug.lower().strip()
        if not slug.replace("-", "").isalnum():
            raise HTTPException(400, "tenant_slug must be alphanumeric (dashes allowed)")
        
        # Check if tenant exists
        existing = await db.execute(select(Tenant).where(Tenant.slug == slug))
        tenant = existing.scalar_one_or_none()
        
        if tenant is None:
            tenant = Tenant(
                name=req.tenant_name or req.full_name,
                slug=slug,
                plan=TenantPlan.FREE,
            )
            db.add(tenant)
            await db.flush()
    else:
        raise HTTPException(400, "Direct signup only for consultants. Students/clients join via invitation.")
    
    # Check if email already exists in tenant
    existing_user = await db.execute(
        select(User).where(User.tenant_id == tenant.id, User.email == req.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(409, "Email already registered in this tenant")
    
    # Create user
    user = User(
        tenant_id=tenant.id,
        email=req.email,
        password_hash=hash_password(req.password),
        full_name=req.full_name,
        phone=req.phone,
        role=req.role,
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Generate tokens
    token_data = {"sub": user.id, "role": user.role.value, "tenant_id": user.tenant_id}
    
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user_id=user.id,
        role=user.role.value,
        tenant_id=user.tenant_id,
    )


# ==========================================
# LOGIN
# ==========================================
@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate user, return JWT tokens."""
    # Find user by email (across all tenants - email should be unique enough for login)
    result = await db.execute(select(User).where(User.email == req.email))
    users = result.scalars().all()
    
    if not users:
        raise HTTPException(401, "Invalid credentials")
    
    # For simplicity, use first match. Later add tenant_id to login.
    user = users[0]
    
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(403, "User is inactive")
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    token_data = {"sub": user.id, "role": user.role.value, "tenant_id": user.tenant_id}
    
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user_id=user.id,
        role=user.role.value,
        tenant_id=user.tenant_id,
    )


# ==========================================
# REFRESH
# ==========================================
@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Get new access token from refresh token."""
    payload = decode_token(req.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(401, "User not found or inactive")
    
    token_data = {"sub": user.id, "role": user.role.value, "tenant_id": user.tenant_id}
    
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user_id=user.id,
        role=user.role.value,
        tenant_id=user.tenant_id,
    )


# ==========================================
# ME (current user)
# ==========================================
@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser):
    """Return current authenticated user's info."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
        tenant_id=current_user.tenant_id,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
    )
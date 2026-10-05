"""
VASTU ONE - Client Routes
==========================
CRUD for clients (tenant-scoped).
"""
from __future__ import annotations
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Client, User, UserRole


router = APIRouter(prefix="/api/clients", tags=["clients"])


# ==========================================
# SCHEMAS
# ==========================================
class ClientCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    notes: str | None = None


class ClientUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    notes: str | None = None


class ClientResponse(BaseModel):
    id: str
    tenant_id: str
    consultant_id: str | None
    full_name: str
    email: str | None
    phone: str | None
    address: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    total: int
    items: list[ClientResponse]


# ==========================================
# CREATE
# ==========================================
@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    req: ClientCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Create a new client under the consultant's tenant."""
    client = Client(
        tenant_id=current_user.tenant_id,
        consultant_id=current_user.id,
        full_name=req.full_name,
        email=req.email,
        phone=req.phone,
        address=req.address,
        notes=req.notes,
    )
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client


# ==========================================
# LIST
# ==========================================
@router.get("", response_model=ClientListResponse)
async def list_clients(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = Query(None, max_length=100),
):
    """List clients for the current tenant."""
    stmt = select(Client).where(Client.tenant_id == current_user.tenant_id)
    
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            (Client.full_name.ilike(pattern)) | (Client.email.ilike(pattern)) | (Client.phone.ilike(pattern))
        )
    
    # Total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0
    
    # Items
    stmt = stmt.order_by(Client.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    return ClientListResponse(total=total, items=list(items))


# ==========================================
# GET ONE
# ==========================================
@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get a single client by ID (tenant-scoped)."""
    stmt = select(Client).where(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id,
    )
    client = (await db.execute(stmt)).scalar_one_or_none()
    if not client:
        raise HTTPException(404, "Client not found")
    return client


# ==========================================
# UPDATE
# ==========================================
@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: str,
    req: ClientUpdate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Update a client."""
    stmt = select(Client).where(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id,
    )
    client = (await db.execute(stmt)).scalar_one_or_none()
    if not client:
        raise HTTPException(404, "Client not found")
    
    # Update only provided fields
    data = req.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(client, key, value)
    
    await db.commit()
    await db.refresh(client)
    return client


# ==========================================
# DELETE
# ==========================================
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: str,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Delete a client (cascade deletes properties/reports)."""
    stmt = select(Client).where(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id,
    )
    client = (await db.execute(stmt)).scalar_one_or_none()
    if not client:
        raise HTTPException(404, "Client not found")
    
    await db.delete(client)
    await db.commit()
    return None
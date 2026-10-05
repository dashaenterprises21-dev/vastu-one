"""
VASTU ONE - Property Routes
============================
CRUD for properties (scoped to client + tenant).
"""
from __future__ import annotations
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Client, Property, PropertyType


router = APIRouter(prefix="/api/properties", tags=["properties"])


# ==========================================
# SCHEMAS
# ==========================================
class PropertyCreate(BaseModel):
    client_id: str
    name: str = Field(..., min_length=2, max_length=255)
    property_type: PropertyType = PropertyType.RESIDENTIAL
    address: str | None = None
    city: str | None = Field(None, max_length=100)
    pincode: str | None = Field(None, max_length=10)
    latitude: float | None = None
    longitude: float | None = None
    north_direction_deg: float | None = Field(None, ge=0, le=360)


class PropertyUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    property_type: PropertyType | None = None
    address: str | None = None
    city: str | None = Field(None, max_length=100)
    pincode: str | None = Field(None, max_length=10)
    latitude: float | None = None
    longitude: float | None = None
    floor_plan_url: str | None = None
    north_direction_deg: float | None = Field(None, ge=0, le=360)


class PropertyResponse(BaseModel):
    id: str
    client_id: str
    name: str
    property_type: str
    address: str | None
    city: str | None
    pincode: str | None
    latitude: float | None
    longitude: float | None
    floor_plan_url: str | None
    north_direction_deg: float | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PropertyListResponse(BaseModel):
    total: int
    items: list[PropertyResponse]


# ==========================================
# CREATE
# ==========================================
@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    req: PropertyCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Create a property under a client."""
    # Verify client belongs to this tenant
    stmt = select(Client).where(
        Client.id == req.client_id,
        Client.tenant_id == current_user.tenant_id,
    )
    client = (await db.execute(stmt)).scalar_one_or_none()
    if not client:
        raise HTTPException(404, "Client not found in your tenant")
    
    prop = Property(
        client_id=req.client_id,
        name=req.name,
        property_type=req.property_type,
        address=req.address,
        city=req.city,
        pincode=req.pincode,
        latitude=req.latitude,
        longitude=req.longitude,
        north_direction_deg=req.north_direction_deg,
    )
    db.add(prop)
    await db.commit()
    await db.refresh(prop)
    return prop


# ==========================================
# LIST
# ==========================================
@router.get("", response_model=PropertyListResponse)
async def list_properties(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    client_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    """List properties in current tenant (optionally filter by client)."""
    # Join with clients to ensure tenant scoping
    stmt = select(Property).join(Client).where(Client.tenant_id == current_user.tenant_id)
    
    if client_id:
        stmt = stmt.where(Property.client_id == client_id)
    
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0
    
    stmt = stmt.order_by(Property.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    return PropertyListResponse(total=total, items=list(items))


# ==========================================
# GET ONE
# ==========================================
@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get single property (tenant-scoped)."""
    stmt = (
        select(Property)
        .join(Client)
        .where(Property.id == property_id, Client.tenant_id == current_user.tenant_id)
    )
    prop = (await db.execute(stmt)).scalar_one_or_none()
    if not prop:
        raise HTTPException(404, "Property not found")
    return prop


# ==========================================
# UPDATE
# ==========================================
@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: str,
    req: PropertyUpdate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Update property."""
    stmt = (
        select(Property)
        .join(Client)
        .where(Property.id == property_id, Client.tenant_id == current_user.tenant_id)
    )
    prop = (await db.execute(stmt)).scalar_one_or_none()
    if not prop:
        raise HTTPException(404, "Property not found")
    
    data = req.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(prop, key, value)
    
    await db.commit()
    await db.refresh(prop)
    return prop


# ==========================================
# DELETE
# ==========================================
@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: str,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Delete property."""
    stmt = (
        select(Property)
        .join(Client)
        .where(Property.id == property_id, Client.tenant_id == current_user.tenant_id)
    )
    prop = (await db.execute(stmt)).scalar_one_or_none()
    if not prop:
        raise HTTPException(404, "Property not found")
    
    await db.delete(prop)
    await db.commit()
    return None
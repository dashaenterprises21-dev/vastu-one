"""
VASTU ONE - Ecommerce Routes
==============================
Products, Orders, Cart.
"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Product, Order


router = APIRouter(prefix="/api/ecommerce", tags=["ecommerce"])


# ==========================================
# SCHEMAS
# ==========================================
class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    category: str = Field(..., max_length=50)
    price_inr: float = Field(..., ge=0)
    stock_qty: int = Field(0, ge=0)
    image_url: str | None = None


class ProductResponse(BaseModel):
    id: str
    tenant_id: str | None
    sku: str
    name: str
    description: str | None
    category: str
    price_inr: float
    stock_qty: int
    image_url: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: list[dict]
    shipping_address: dict = Field(default_factory=dict)


class OrderResponse(BaseModel):
    id: str
    tenant_id: str
    user_id: str | None
    total_inr: float
    status: str
    items: list
    shipping_address: dict
    razorpay_order_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# PRODUCTS
# ==========================================
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    req: ProductCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Create a product."""
    # Check SKU uniqueness
    existing = await db.execute(select(Product).where(Product.sku == req.sku))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "SKU already in use")
    
    product = Product(tenant_id=current_user.tenant_id, **req.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@router.get("/products", response_model=list[ProductResponse])
async def list_products(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    category: str | None = Query(None),
    active_only: bool = Query(True),
):
    """List products."""
    stmt = select(Product).where(Product.tenant_id == current_user.tenant_id)
    if category:
        stmt = stmt.where(Product.category == category)
    if active_only:
        stmt = stmt.where(Product.is_active == True)
    stmt = stmt.order_by(Product.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Product).where(
        Product.id == product_id,
        Product.tenant_id == current_user.tenant_id,
    )
    product = (await db.execute(stmt)).scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")
    return product


# ==========================================
# ORDERS
# ==========================================
@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    req: OrderCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Create an order from cart items."""
    if not req.items:
        raise HTTPException(400, "Order must have at least one item")
    
    # Calculate total
    total = sum(float(item.get("price_inr", 0)) * int(item.get("quantity", 1)) for item in req.items)
    
    order = Order(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        total_inr=total,
        status="pending",
        items=req.items,
        shipping_address=req.shipping_address,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/orders", response_model=list[OrderResponse])
async def list_orders(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Order).where(
        Order.tenant_id == current_user.tenant_id,
        Order.user_id == current_user.id,
    ).order_by(Order.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Order).where(
        Order.id == order_id,
        Order.user_id == current_user.id,
    )
    order = (await db.execute(stmt)).scalar_one_or_none()
    if not order:
        raise HTTPException(404, "Order not found")
    return order
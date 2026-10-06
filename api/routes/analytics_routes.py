"""
VASTU ONE - Analytics API
===========================
Business intelligence stats for dashboard v2.
"""
from __future__ import annotations
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from database.base import get_db
from database.models import Client, Property, Report, Order, User


router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
async def get_overview(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """High-level business metrics."""
    tenant_id = current_user.tenant_id
    
    # Counts
    clients_count = (await db.execute(
        select(func.count(Client.id)).where(Client.tenant_id == tenant_id)
    )).scalar() or 0
    
    properties_count = (await db.execute(
        select(func.count(Property.id))
        .join(Client, Property.client_id == Client.id)
        .where(Client.tenant_id == tenant_id)
    )).scalar() or 0
    
    reports_count = (await db.execute(
        select(func.count(Report.id))
        .join(Property, Report.property_id == Property.id)
        .join(Client, Property.client_id == Client.id)
        .where(Client.tenant_id == tenant_id)
    )).scalar() or 0
    
    # Revenue from reports
    report_revenue = (await db.execute(
        select(func.coalesce(func.sum(Report.price_inr), 0))
        .join(Property, Report.property_id == Property.id)
        .join(Client, Property.client_id == Client.id)
        .where(Client.tenant_id == tenant_id)
    )).scalar() or 0
    
    # Orders revenue (paid only)
    order_revenue = (await db.execute(
        select(func.coalesce(func.sum(Order.total_inr), 0))
        .where(
            Order.tenant_id == tenant_id,
            Order.status == "paid",
        )
    )).scalar() or 0
    
    total_revenue = float(report_revenue) + float(order_revenue)
    
    # Active users (last 30 days)
    last_30 = datetime.utcnow() - timedelta(days=30)
    active_users = (await db.execute(
        select(func.count(User.id)).where(
            User.tenant_id == tenant_id,
            User.last_login >= last_30,
        )
    )).scalar() or 0
    
    return {
        "clients_count": clients_count,
        "properties_count": properties_count,
        "reports_count": reports_count,
        "total_revenue": round(total_revenue, 2),
        "report_revenue": round(float(report_revenue), 2),
        "order_revenue": round(float(order_revenue), 2),
        "active_users_30d": active_users,
    }


@router.get("/revenue-timeline")
async def get_revenue_timeline(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    days: int = Query(30, ge=7, le=90),
):
    """Revenue over time (last N days)."""
    tenant_id = current_user.tenant_id
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily revenue from reports
    report_query = text("""
        SELECT DATE(r.created_at) as day, COALESCE(SUM(r.price_inr), 0) as revenue
        FROM reports r
        JOIN properties p ON r.property_id = p.id
        JOIN clients c ON p.client_id = c.id
        WHERE c.tenant_id = :tenant_id
        AND r.created_at >= :start_date
        GROUP BY DATE(r.created_at)
        ORDER BY day
    """)
    
    report_rows = (await db.execute(report_query, {
        "tenant_id": tenant_id,
        "start_date": start_date,
    })).all()
    
    # Daily revenue from orders
    order_query = text("""
        SELECT DATE(created_at) as day, COALESCE(SUM(total_inr), 0) as revenue
        FROM orders
        WHERE tenant_id = :tenant_id
        AND status = 'paid'
        AND created_at >= :start_date
        GROUP BY DATE(created_at)
        ORDER BY day
    """)
    
    order_rows = (await db.execute(order_query, {
        "tenant_id": tenant_id,
        "start_date": start_date,
    })).all()
    
    # Combine
    combined = {}
    for row in report_rows:
        day_str = row.day.isoformat() if hasattr(row.day, 'isoformat') else str(row.day)
        combined[day_str] = combined.get(day_str, 0) + float(row.revenue)
    for row in order_rows:
        day_str = row.day.isoformat() if hasattr(row.day, 'isoformat') else str(row.day)
        combined[day_str] = combined.get(day_str, 0) + float(row.revenue)
    
    return {
        "timeline": [
            {"date": day, "revenue": round(rev, 2)}
            for day, rev in sorted(combined.items())
        ]
    }


@router.get("/reports-by-package")
async def get_reports_by_package(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Report counts grouped by package."""
    tenant_id = current_user.tenant_id
    
    query = text("""
        SELECT r.package, COUNT(*) as count, COALESCE(SUM(r.price_inr), 0) as revenue
        FROM reports r
        JOIN properties p ON r.property_id = p.id
        JOIN clients c ON p.client_id = c.id
        WHERE c.tenant_id = :tenant_id
        GROUP BY r.package
        ORDER BY count DESC
    """)
    
    rows = (await db.execute(query, {"tenant_id": tenant_id})).all()
    
    return {
        "packages": [
            {
                "package": row.package,
                "count": row.count,
                "revenue": round(float(row.revenue), 2),
            }
            for row in rows
        ]
    }


@router.get("/clients-growth")
async def get_clients_growth(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    days: int = Query(30, ge=7, le=90),
):
    """Client growth over time."""
    tenant_id = current_user.tenant_id
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = text("""
        SELECT DATE(created_at) as day, COUNT(*) as count
        FROM clients
        WHERE tenant_id = :tenant_id
        AND created_at >= :start_date
        GROUP BY DATE(created_at)
        ORDER BY day
    """)
    
    rows = (await db.execute(query, {
        "tenant_id": tenant_id,
        "start_date": start_date,
    })).all()
    
    return {
        "growth": [
            {
                "date": row.day.isoformat() if hasattr(row.day, 'isoformat') else str(row.day),
                "count": row.count,
            }
            for row in rows
        ]
    }


@router.get("/orders-status")
async def get_orders_status(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Order counts by status."""
    tenant_id = current_user.tenant_id
    
    query = text("""
        SELECT status, COUNT(*) as count, COALESCE(SUM(total_inr), 0) as revenue
        FROM orders
        WHERE tenant_id = :tenant_id
        GROUP BY status
        ORDER BY count DESC
    """)
    
    rows = (await db.execute(query, {"tenant_id": tenant_id})).all()
    
    return {
        "statuses": [
            {
                "status": row.status,
                "count": row.count,
                "revenue": round(float(row.revenue), 2),
            }
            for row in rows
        ]
    }


@router.get("/activity-heatmap")
async def get_activity_heatmap(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Hourly activity (last 7 days) for heatmap."""
    tenant_id = current_user.tenant_id
    
    query = text("""
        SELECT 
            EXTRACT(DOW FROM created_at) as day_of_week,
            EXTRACT(HOUR FROM created_at) as hour,
            COUNT(*) as count
        FROM audit_logs
        WHERE tenant_id = :tenant_id
        AND created_at >= NOW() - INTERVAL '7 days'
        GROUP BY day_of_week, hour
        ORDER BY day_of_week, hour
    """)
    
    rows = (await db.execute(query, {"tenant_id": tenant_id})).all()
    
    return {
        "heatmap": [
            {
                "day": int(row.day_of_week),
                "hour": int(row.hour),
                "count": row.count,
            }
            for row in rows
        ]
    }
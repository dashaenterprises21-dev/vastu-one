"""
VASTU ONE - Sentinel Admin API
================================
Aggregated security stats from audit_logs.
"""
from __future__ import annotations
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import RequireConsultant
from database.base import get_db
from database.models import AuditLog


router = APIRouter(prefix="/api/sentinel", tags=["sentinel"])


@router.get("/stats")
async def get_security_stats(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Overall security statistics."""
    from sqlalchemy import text
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    # Total requests today
    total_query = text("SELECT COUNT(*) FROM audit_logs WHERE created_at >= :today")
    total_requests = (await db.execute(total_query, {"today": today_start})).scalar() or 0
    
    # Failed logins today (401 on /api/auth/login)
    failed_query = text("""
        SELECT COUNT(*) FROM audit_logs 
        WHERE created_at >= :today 
        AND action = 'CLIENT_ERROR'
        AND details->>'path' = '/api/auth/login'
        AND details->>'status' = '401'
    """)
    failed_logins = (await db.execute(failed_query, {"today": today_start})).scalar() or 0
    
    # Rate limited (429)
    blocked_query = text("""
        SELECT COUNT(*) FROM audit_logs 
        WHERE created_at >= :today 
        AND details->>'status' = '429'
    """)
    blocked_requests = (await db.execute(blocked_query, {"today": today_start})).scalar() or 0
    
    # Suspicious requests
    sus_query = text("""
        SELECT COUNT(*) FROM audit_logs 
        WHERE created_at >= :today 
        AND details->>'suspicious' = 'true'
    """)
    suspicious_requests = (await db.execute(sus_query, {"today": today_start})).scalar() or 0
    
    # Server errors (5xx) last 24h
    err_query = text("""
        SELECT COUNT(*) FROM audit_logs 
        WHERE created_at >= :last24 
        AND action = 'SERVER_ERROR'
    """)
    server_errors = (await db.execute(err_query, {"last24": last_24h})).scalar() or 0
    
    return {
        "total_requests_today": total_requests,
        "failed_logins_today": failed_logins,
        "blocked_by_rate_limit_today": blocked_requests,
        "suspicious_requests_today": suspicious_requests,
        "server_errors_24h": server_errors,
    }


@router.get("/recent-activity")
async def get_recent_activity(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
):
    """Recent requests for activity feed."""
    stmt = select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)
    logs = (await db.execute(stmt)).scalars().all()
    
    return {
        "activities": [
            {
                "id": log.id,
                "action": log.action,
                "path": (log.details or {}).get("path", ""),
                "method": (log.details or {}).get("method", ""),
                "status": (log.details or {}).get("status", 0),
                "duration_ms": (log.details or {}).get("duration_ms", 0),
                "suspicious": (log.details or {}).get("suspicious", False),
                "ip_address": log.ip_address,
                "user_id": log.user_id,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ]
    }


@router.get("/top-ips")
async def get_top_ips(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=50),
):
    """Top IP addresses by request count (today)."""
    from sqlalchemy import text
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    query = text("""
        SELECT 
            ip_address,
            COUNT(*) as request_count,
            SUM(CASE WHEN details->>'suspicious' = 'true' THEN 1 ELSE 0 END) as suspicious_count
        FROM audit_logs
        WHERE created_at >= :today
        GROUP BY ip_address
        ORDER BY request_count DESC
        LIMIT :lim
    """)
    
    rows = (await db.execute(query, {"today": today_start, "lim": limit})).all()
    
    return {
        "top_ips": [
            {
                "ip_address": row.ip_address or "unknown",
                "request_count": row.request_count,
                "suspicious_count": row.suspicious_count or 0,
            }
            for row in rows
        ]
    }


@router.get("/audit-logs")
async def get_audit_logs(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
    action_filter: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
):
    """Paginated audit logs."""
    stmt = select(AuditLog).order_by(desc(AuditLog.created_at))
    
    if action_filter:
        stmt = stmt.where(AuditLog.action.ilike(f"%{action_filter}%"))
    
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0
    
    stmt = stmt.offset(skip).limit(limit)
    logs = (await db.execute(stmt)).scalars().all()
    
    return {
        "total": total,
        "logs": [
            {
                "id": log.id,
                "action": log.action,
                "entity_type": log.entity_type,
                "user_id": log.user_id,
                "ip_address": log.ip_address,
                "details": log.details,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ],
    }
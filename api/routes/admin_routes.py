"""
VASTU ONE — Enterprise Admin Routes
====================================
Complete admin panel backend API.

Endpoints:
  /api/admin/stats                    → Dashboard KPIs
  /api/admin/users                    → User management
  /api/admin/users/{id}               → User detail/update
  /api/admin/courses                  → Course management
  /api/admin/enrollments              → Enrollment list
  /api/admin/orders                   → Payment/order list
  /api/admin/revenue/timeline         → Revenue chart data
  /api/admin/activity/recent          → Recent activity feed
  /api/admin/sentinel/overview        → Security stats
  /api/admin/health                   → System health
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, func, desc, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from database.base import get_db
from database.models import (
    User, Course, CourseSection, Lesson, Enrollment,
    Order, LessonProgress, Certificate
)


router = APIRouter(prefix="/api/admin", tags=["admin"])


# ============================================================
# PERMISSIONS
# ============================================================

def require_admin(user: CurrentUser):
    """Verify admin access."""
    role = user.role.value if hasattr(user.role, "value") else str(user.role)
    if role.upper() not in ("ADMIN", "SUPER_ADMIN", "CONSULTANT"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


# ============================================================
# 1. DASHBOARD STATS
# ============================================================

@router.get("/stats")
async def get_dashboard_stats(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Overall platform KPIs."""
    require_admin(current_user)

    # Total counts
    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
    total_courses = (await db.execute(select(func.count(Course.id)))).scalar() or 0
    total_enrollments = (await db.execute(select(func.count(Enrollment.id)))).scalar() or 0
    total_lessons = (await db.execute(select(func.count(Lesson.id)))).scalar() or 0
    total_sections = (await db.execute(select(func.count(CourseSection.id)))).scalar() or 0
    total_certificates = (await db.execute(select(func.count(Certificate.id)))).scalar() or 0

    # Revenue
    revenue_result = await db.execute(
        select(func.coalesce(func.sum(Order.total_inr), 0))
        .where(Order.status.in_(["paid", "captured", "success"]))
    )
    total_revenue = float(revenue_result.scalar() or 0)

    # Active users (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = (await db.execute(
        select(func.count(func.distinct(Enrollment.student_id)))
        .where(Enrollment.enrolled_at >= thirty_days_ago)
    )).scalar() or 0

    # Today's new signups
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    new_today = (await db.execute(
        select(func.count(User.id)).where(User.created_at >= today)
    )).scalar() or 0

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_lessons": total_lessons,
        "total_sections": total_sections,
        "total_certificates": total_certificates,
        "total_revenue": total_revenue,
        "active_users_30d": active_users,
        "new_signups_today": new_today,
    }


# ============================================================
# 2. USERS MANAGEMENT
# ============================================================

@router.get("/users")
async def list_users(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: int = Query(50, le=500),
    offset: int = 0,
):
    """List users with filters."""
    require_admin(current_user)

    stmt = select(User)

    if search:
        stmt = stmt.where(or_(
            User.email.ilike(f"%{search}%"),
            User.full_name.ilike(f"%{search}%"),
        ))
    if role:
        stmt = stmt.where(User.role == role)
    if is_active is not None:
        stmt = stmt.where(User.is_active == is_active)

    # Total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = stmt.order_by(desc(User.created_at)).offset(offset).limit(limit)
    users = (await db.execute(stmt)).scalars().all()

    return {
        "total": total,
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "phone": u.phone,
                "role": u.role.value if hasattr(u.role, "value") else str(u.role),
                "is_active": u.is_active,
                "is_verified": u.is_verified,
                "last_login": u.last_login.isoformat() if u.last_login else None,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
    }


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


@router.patch("/users/{user_id}")
async def update_user(
    user_id: str,
    req: UserUpdateRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Update user details."""
    require_admin(current_user)

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    if req.full_name is not None:
        user.full_name = req.full_name
    if req.role is not None:
        user.role = req.role
    if req.is_active is not None:
        user.is_active = req.is_active
    if req.is_verified is not None:
        user.is_verified = req.is_verified

    await db.commit()
    await db.refresh(user)

    return {"ok": True, "user_id": user.id}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Soft-delete user (deactivate)."""
    require_admin(current_user)

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    if user.id == current_user.id:
        raise HTTPException(400, "Cannot deactivate yourself")

    user.is_active = False
    await db.commit()

    return {"ok": True, "message": f"User {user.email} deactivated"}


# ============================================================
# 3. COURSES MANAGEMENT
# ============================================================

@router.get("/courses")
async def list_courses(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """List all courses with stats."""
    require_admin(current_user)

    stmt = select(Course).order_by(desc(Course.created_at))
    courses = (await db.execute(stmt)).scalars().all()

    result = []
    for c in courses:
        # Counts per course
        sec_count = (await db.execute(
            select(func.count(CourseSection.id)).where(CourseSection.course_id == c.id)
        )).scalar() or 0

        les_count = (await db.execute(
            select(func.count(Lesson.id))
            .join(CourseSection, Lesson.section_id == CourseSection.id)
            .where(CourseSection.course_id == c.id)
        )).scalar() or 0

        enr_count = (await db.execute(
            select(func.count(Enrollment.id)).where(Enrollment.course_id == c.id)
        )).scalar() or 0

        result.append({
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "language": c.language,
            "price_inr": float(c.price_inr or 0),
            "duration_weeks": c.duration_weeks,
            "is_published": c.is_published,
            "sections_count": sec_count,
            "lessons_count": les_count,
            "enrollments_count": enr_count,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        })

    return {"total": len(result), "courses": result}


@router.patch("/courses/{course_id}/publish")
async def toggle_course_publish(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Toggle course published status."""
    require_admin(current_user)

    course = (await db.execute(select(Course).where(Course.id == course_id))).scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found")

    course.is_published = not course.is_published
    await db.commit()

    return {"ok": True, "is_published": course.is_published}


# ============================================================
# 4. ENROLLMENTS
# ============================================================

@router.get("/enrollments")
async def list_enrollments(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(100, le=500),
    offset: int = 0,
):
    """List all enrollments."""
    require_admin(current_user)

    stmt = (
        select(Enrollment, User, Course)
        .join(User, Enrollment.student_id == User.id)
        .join(Course, Enrollment.course_id == Course.id)
        .order_by(desc(Enrollment.enrolled_at))
        .offset(offset)
        .limit(limit)
    )
    rows = (await db.execute(stmt)).all()

    return {
        "enrollments": [
            {
                "id": e.Enrollment.id,
                "student_email": e.User.email,
                "student_name": e.User.full_name,
                "course_title": e.Course.title,
                "course_id": e.Course.id,
                "progress_pct": float(e.Enrollment.progress_pct or 0),
                "status": getattr(e.Enrollment, "status", "active"),
                "created_at": e.Enrollment.enrolled_at.isoformat() if e.Enrollment.enrolled_at else None,
            }
            for e in rows
        ],
    }


# ============================================================
# 5. ORDERS / PAYMENTS
# ============================================================

@router.get("/orders")
async def list_orders(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(100, le=500),
    offset: int = 0,
):
    """List all orders."""
    require_admin(current_user)

    stmt = select(Order)
    if status_filter:
        stmt = stmt.where(Order.status == status_filter)
    stmt = stmt.order_by(desc(Order.created_at)).offset(offset).limit(limit)

    orders = (await db.execute(stmt)).scalars().all()

    return {
        "orders": [
            {
                "id": o.id,
                "amount_inr": float(o.total_inr or 0),
                "status": o.status,
                "razorpay_order_id": getattr(o, "razorpay_order_id", None),
                "razorpay_payment_id": getattr(o, "razorpay_payment_id", None),
                "user_id": getattr(o, "user_id", None),
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in orders
        ],
    }


# ============================================================
# 6. REVENUE TIMELINE (Chart Data)
# ============================================================

@router.get("/revenue/timeline")
async def revenue_timeline(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    days: int = Query(30, le=365),
):
    """Revenue over last N days for charts."""
    require_admin(current_user)

    since = datetime.utcnow() - timedelta(days=days)

    # Simple daily aggregation
    stmt = (
        select(
            func.date_trunc("day", Order.created_at).label("day"),
            func.sum(Order.total_inr).label("revenue"),
            func.count(Order.id).label("orders"),
        )
        .where(and_(
            Order.created_at >= since,
            Order.status.in_(["paid", "captured", "success"]),
        ))
        .group_by(text("day"))
        .order_by(text("day"))
    )
    rows = (await db.execute(stmt)).all()

    return {
        "days": days,
        "data": [
            {
                "date": row.day.isoformat() if row.day else None,
                "revenue": float(row.revenue or 0),
                "orders": row.orders or 0,
            }
            for row in rows
        ],
    }


# ============================================================
# 7. RECENT ACTIVITY
# ============================================================

@router.get("/activity/recent")
async def recent_activity(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, le=100),
):
    """Recent platform activity."""
    require_admin(current_user)

    activities = []

    # Recent signups
    recent_users = (await db.execute(
        select(User).order_by(desc(User.created_at)).limit(limit)
    )).scalars().all()
    for u in recent_users:
        activities.append({
            "type": "signup",
            "icon": "user-plus",
            "title": f"New user: {u.email}",
            "subtitle": u.full_name or "—",
            "timestamp": u.created_at.isoformat() if u.created_at else None,
        })

    # Recent enrollments
    stmt = (
        select(Enrollment, User, Course)
        .join(User, Enrollment.student_id == User.id)
        .join(Course, Enrollment.course_id == Course.id)
        .order_by(desc(Enrollment.enrolled_at))
        .limit(limit)
    )
    recent_enrolls = (await db.execute(stmt)).all()
    for e in recent_enrolls:
        activities.append({
            "type": "enrollment",
            "icon": "book-open",
            "title": f"Enrolled: {e.User.email}",
            "subtitle": e.Course.title,
            "timestamp": e.Enrollment.enrolled_at.isoformat() if e.Enrollment.enrolled_at else None,
        })

    # Recent orders
    recent_orders = (await db.execute(
        select(Order).order_by(desc(Order.created_at)).limit(limit)
    )).scalars().all()
    for o in recent_orders:
        activities.append({
            "type": "order",
            "icon": "shopping-cart",
            "title": f"Order: ₹{float(o.total_inr or 0):,.0f}",
            "subtitle": f"Status: {o.status}",
            "timestamp": o.created_at.isoformat() if o.created_at else None,
        })

    # Sort by timestamp desc
    activities.sort(key=lambda x: x["timestamp"] or "", reverse=True)

    return {"activities": activities[:limit]}


# ============================================================
# 8. SENTINEL OVERVIEW
# ============================================================

@router.get("/sentinel/overview")
async def sentinel_overview(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Security overview stats."""
    require_admin(current_user)

    # Placeholder — extend with real audit log queries
    return {
        "rate_limited_requests_24h": 0,
        "blocked_ips": 0,
        "failed_logins_24h": 0,
        "suspicious_activity": 0,
        "status": "active",
    }


# ============================================================
# 9. SYSTEM HEALTH
# ============================================================

@router.get("/health")
async def system_health(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """System health check."""
    require_admin(current_user)

    # DB check
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "database": "healthy" if db_ok else "unhealthy",
        "api": "healthy",
        "sentinel": "active",
        "timestamp": datetime.utcnow().isoformat(),
    }
"""
VASTU ONE - LMS v2: Instructor Dashboard
==========================================
Aggregated stats for instructor's academy.
"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import RequireConsultant
from database.base import get_db
from database.models import (
    Course, CourseSection, Lesson, Enrollment, LessonProgress,
    CourseReview, User,
)


router = APIRouter(prefix="/api/lms/v2/instructor", tags=["lms-v2-instructor"])


@router.get("/stats")
async def get_instructor_stats(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated stats for instructor."""
    tenant_id = current_user.tenant_id
    
    # Total courses
    courses_stmt = select(func.count(Course.id)).where(Course.tenant_id == tenant_id)
    total_courses = (await db.execute(courses_stmt)).scalar() or 0
    
    # Get all course IDs
    course_ids_stmt = select(Course.id).where(Course.tenant_id == tenant_id)
    course_ids = [row[0] for row in (await db.execute(course_ids_stmt)).all()]
    
    # Total students (unique enrollments)
    total_students = 0
    total_revenue = 0.0
    if course_ids:
        students_stmt = select(func.count(func.distinct(Enrollment.student_id))).where(
            Enrollment.course_id.in_(course_ids)
        )
        total_students = (await db.execute(students_stmt)).scalar() or 0
        
        # Revenue estimate (enrollments × course price)
        revenue_stmt = select(func.sum(Course.price_inr)).select_from(
            Enrollment
        ).join(Course, Enrollment.course_id == Course.id).where(
            Course.tenant_id == tenant_id
        )
        total_revenue = float((await db.execute(revenue_stmt)).scalar() or 0)
    
    # Average rating
    avg_rating = 0.0
    if course_ids:
        rating_stmt = select(func.avg(CourseReview.rating)).where(
            CourseReview.course_id.in_(course_ids)
        )
        avg_rating = float((await db.execute(rating_stmt)).scalar() or 0)
    
    # Average student progress
    avg_progress = 0.0
    if course_ids:
        progress_stmt = select(func.avg(Enrollment.progress_pct)).where(
            Enrollment.course_id.in_(course_ids)
        )
        avg_progress = float((await db.execute(progress_stmt)).scalar() or 0)
    
    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_revenue": round(total_revenue, 2),
        "average_rating": round(avg_rating, 2),
        "average_progress": round(avg_progress, 1),
    }


@router.get("/courses")
async def list_instructor_courses(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """List instructor's courses with stats."""
    tenant_id = current_user.tenant_id
    
    stmt = select(Course).where(Course.tenant_id == tenant_id).order_by(Course.created_at.desc())
    courses = (await db.execute(stmt)).scalars().all()
    
    result = []
    for course in courses:
        # Students count
        students_stmt = select(func.count(Enrollment.id)).where(Enrollment.course_id == course.id)
        students = (await db.execute(students_stmt)).scalar() or 0
        
        # Avg progress
        avg_stmt = select(func.avg(Enrollment.progress_pct)).where(Enrollment.course_id == course.id)
        avg_progress = float((await db.execute(avg_stmt)).scalar() or 0)
        
        # Rating
        rating_stmt = select(func.avg(CourseReview.rating)).where(CourseReview.course_id == course.id)
        avg_rating = float((await db.execute(rating_stmt)).scalar() or 0)
        
        # Revenue
        revenue = students * course.price_inr
        
        result.append({
            "id": course.id,
            "title": course.title,
            "is_published": course.is_published,
            "price_inr": course.price_inr,
            "students": students,
            "avg_progress": round(avg_progress, 1),
            "avg_rating": round(avg_rating, 2),
            "revenue": round(revenue, 2),
            "created_at": course.created_at.isoformat(),
        })
    
    return {"courses": result}


@router.get("/students")
async def list_instructor_students(
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
    limit: int = 20,
):
    """List recent students across all courses."""
    tenant_id = current_user.tenant_id
    
    # Get course IDs
    course_ids_stmt = select(Course.id).where(Course.tenant_id == tenant_id)
    course_ids = [row[0] for row in (await db.execute(course_ids_stmt)).all()]
    
    if not course_ids:
        return {"students": []}
    
    # Recent enrollments
    stmt = select(Enrollment, User, Course).join(
        User, Enrollment.student_id == User.id
    ).join(
        Course, Enrollment.course_id == Course.id
    ).where(
        Enrollment.course_id.in_(course_ids)
    ).order_by(Enrollment.enrolled_at.desc()).limit(limit)
    
    rows = (await db.execute(stmt)).all()
    
    return {
        "students": [
            {
                "student_id": user.id,
                "name": user.full_name,
                "email": user.email,
                "course_id": course.id,
                "course_title": course.title,
                "enrolled_at": enrollment.enrolled_at.isoformat(),
                "progress_pct": enrollment.progress_pct,
                "last_login": user.last_login.isoformat() if user.last_login else None,
            }
            for enrollment, user, course in rows
        ]
    }
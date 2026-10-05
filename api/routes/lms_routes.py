"""
VASTU ONE - LMS Routes
========================
Courses, Modules, Lessons, Enrollments, Progress, Certificates.
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
from database.models import (
    Course, CourseModule, Lesson, Enrollment, LessonProgress, Certificate,
)


router = APIRouter(prefix="/api/lms", tags=["lms"])


# ==========================================
# SCHEMAS
# ==========================================
class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    thumbnail_url: str | None = None
    language: str = "en"
    duration_weeks: int = 4
    price_inr: float = 0
    is_published: bool = False


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    language: str | None = None
    duration_weeks: int | None = None
    price_inr: float | None = None
    is_published: bool | None = None


class CourseResponse(BaseModel):
    id: str
    tenant_id: str
    instructor_id: str | None
    title: str
    slug: str
    description: str | None
    thumbnail_url: str | None
    language: str
    duration_weeks: int
    price_inr: float
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ModuleCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    order_index: int = 0


class ModuleResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: str | None
    order_index: int
    created_at: datetime

    class Config:
        from_attributes = True


class LessonCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    content_type: str = "video"
    content_url: str | None = None
    text_content: str | None = None
    duration_minutes: int = 0
    order_index: int = 0
    is_preview: bool = False


class LessonResponse(BaseModel):
    id: str
    module_id: str
    title: str
    content_type: str
    content_url: str | None
    text_content: str | None
    duration_minutes: int
    order_index: int
    is_preview: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EnrollResponse(BaseModel):
    id: str
    course_id: str
    student_id: str
    enrolled_at: datetime
    progress_pct: float
    is_active: bool

    class Config:
        from_attributes = True


class ProgressRequest(BaseModel):
    lesson_id: str
    watch_seconds: int = 0
    is_completed: bool = False


# ==========================================
# COURSES
# ==========================================
@router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    req: CourseCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Create a course (consultant only)."""
    # Slug uniqueness
    existing = await db.execute(select(Course).where(Course.slug == req.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Slug already in use")
    
    course = Course(
        tenant_id=current_user.tenant_id,
        instructor_id=current_user.id,
        **req.model_dump(),
    )
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


@router.get("/courses", response_model=list[CourseResponse])
async def list_courses(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    published_only: bool = Query(False),
):
    """List courses in tenant."""
    stmt = select(Course).where(Course.tenant_id == current_user.tenant_id)
    if published_only:
        stmt = stmt.where(Course.is_published == True)
    stmt = stmt.order_by(Course.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Course).where(
        Course.id == course_id,
        Course.tenant_id == current_user.tenant_id,
    )
    course = (await db.execute(stmt)).scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found")
    return course


# ==========================================
# MODULES
# ==========================================
@router.post("/courses/{course_id}/modules", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_module(
    course_id: str,
    req: ModuleCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    # Verify course belongs to tenant
    course_stmt = select(Course).where(
        Course.id == course_id,
        Course.tenant_id == current_user.tenant_id,
    )
    if not (await db.execute(course_stmt)).scalar_one_or_none():
        raise HTTPException(404, "Course not found")
    
    module = CourseModule(course_id=course_id, **req.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


@router.get("/courses/{course_id}/modules", response_model=list[ModuleResponse])
async def list_modules(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(CourseModule)
        .join(Course)
        .where(CourseModule.course_id == course_id, Course.tenant_id == current_user.tenant_id)
        .order_by(CourseModule.order_index)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


# ==========================================
# LESSONS
# ==========================================
@router.post("/modules/{module_id}/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    module_id: str,
    req: LessonCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    # Verify module's course belongs to tenant
    module_stmt = (
        select(CourseModule)
        .join(Course)
        .where(CourseModule.id == module_id, Course.tenant_id == current_user.tenant_id)
    )
    if not (await db.execute(module_stmt)).scalar_one_or_none():
        raise HTTPException(404, "Module not found")
    
    lesson = Lesson(module_id=module_id, **req.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.get("/modules/{module_id}/lessons", response_model=list[LessonResponse])
async def list_lessons(
    module_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Lesson)
        .join(CourseModule)
        .join(Course)
        .where(Lesson.module_id == module_id, Course.tenant_id == current_user.tenant_id)
        .order_by(Lesson.order_index)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


# ==========================================
# ENROLLMENTS
# ==========================================
@router.post("/courses/{course_id}/enroll", response_model=EnrollResponse, status_code=status.HTTP_201_CREATED)
async def enroll(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Enroll current user in a course."""
    # Course must be published
    course_stmt = select(Course).where(
        Course.id == course_id,
        Course.tenant_id == current_user.tenant_id,
        Course.is_published == True,
    )
    course = (await db.execute(course_stmt)).scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found or not published")
    
    # Check duplicate
    existing = await db.execute(
        select(Enrollment).where(
            Enrollment.course_id == course_id,
            Enrollment.student_id == current_user.id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Already enrolled")
    
    enrollment = Enrollment(course_id=course_id, student_id=current_user.id)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


@router.get("/enrollments", response_model=list[EnrollResponse])
async def my_enrollments(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Enrollment).where(Enrollment.student_id == current_user.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


# ==========================================
# PROGRESS
# ==========================================
@router.post("/progress", status_code=status.HTTP_200_OK)
async def mark_progress(
    req: ProgressRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Mark a lesson as watched/completed."""
    # Find enrollment for this lesson
    lesson_stmt = select(Lesson).where(Lesson.id == req.lesson_id)
    lesson = (await db.execute(lesson_stmt)).scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    
    module_stmt = select(CourseModule).where(CourseModule.id == lesson.module_id)
    module = (await db.execute(module_stmt)).scalar_one_or_none()
    
    enroll_stmt = select(Enrollment).where(
        Enrollment.course_id == module.course_id,
        Enrollment.student_id == current_user.id,
    )
    enrollment = (await db.execute(enroll_stmt)).scalar_one_or_none()
    if not enrollment:
        raise HTTPException(403, "Not enrolled in this course")
    
    # Upsert progress
    prog_stmt = select(LessonProgress).where(
        LessonProgress.enrollment_id == enrollment.id,
        LessonProgress.lesson_id == req.lesson_id,
    )
    progress = (await db.execute(prog_stmt)).scalar_one_or_none()
    
    if progress:
        progress.watch_seconds = max(progress.watch_seconds, req.watch_seconds)
        progress.is_completed = progress.is_completed or req.is_completed
        if req.is_completed and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
    else:
        progress = LessonProgress(
            enrollment_id=enrollment.id,
            lesson_id=req.lesson_id,
            watch_seconds=req.watch_seconds,
            is_completed=req.is_completed,
            completed_at=datetime.utcnow() if req.is_completed else None,
        )
        db.add(progress)
    
    await db.commit()
    return {"status": "ok", "lesson_id": req.lesson_id}


# ==========================================
# CERTIFICATE (placeholder)
# ==========================================
@router.get("/enrollments/{enrollment_id}/certificate")
async def get_certificate(
    enrollment_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get certificate metadata (PDF generation later)."""
    stmt = select(Enrollment).where(
        Enrollment.id == enrollment_id,
        Enrollment.student_id == current_user.id,
    )
    enrollment = (await db.execute(stmt)).scalar_one_or_none()
    if not enrollment:
        raise HTTPException(404, "Enrollment not found")
    
    return {
        "enrollment_id": enrollment.id,
        "progress_pct": enrollment.progress_pct,
        "certificate_available": enrollment.progress_pct >= 100.0,
        "message": "Certificate PDF generation coming soon",
    }
"""
VASTU ONE - LMS v2: Course Sections
=====================================
CRUD for course sections (nested inside courses).
"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Course, CourseSection, Lesson


router = APIRouter(prefix="/api/lms/v2/sections", tags=["lms-v2-sections"])


class SectionCreate(BaseModel):
    course_id: str
    title: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    order_index: int = 0


class SectionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    order_index: int | None = None


class SectionResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: str | None
    order_index: int
    duration_minutes: int
    created_at: datetime
    lesson_count: int = 0

    class Config:
        from_attributes = True


@router.post("", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    req: SectionCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Create a new section inside a course."""
    # Verify course belongs to tenant
    course_stmt = select(Course).where(
        Course.id == req.course_id,
        Course.tenant_id == current_user.tenant_id,
    )
    if not (await db.execute(course_stmt)).scalar_one_or_none():
        raise HTTPException(404, "Course not found")

    section = CourseSection(**req.model_dump())
    db.add(section)
    await db.commit()
    await db.refresh(section)
    return SectionResponse(**section.__dict__, lesson_count=0)


@router.get("/by-course/{course_id}", response_model=list[SectionResponse])
async def list_sections_by_course(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """List all sections for a course (with lesson count)."""
    # Verify course belongs to tenant
    course_stmt = select(Course).where(
        Course.id == course_id,
        Course.tenant_id == current_user.tenant_id,
    )
    if not (await db.execute(course_stmt)).scalar_one_or_none():
        raise HTTPException(404, "Course not found")

    stmt = (
        select(CourseSection)
        .where(CourseSection.course_id == course_id)
        .order_by(CourseSection.order_index)
    )
    sections = (await db.execute(stmt)).scalars().all()

    # Get lesson counts
    result = []
    for section in sections:
        count_stmt = select(func.count(Lesson.id)).where(Lesson.section_id == section.id)
        count = (await db.execute(count_stmt)).scalar() or 0
        result.append(SectionResponse(**section.__dict__, lesson_count=count))

    return result


@router.put("/{section_id}", response_model=SectionResponse)
async def update_section(
    section_id: str,
    req: SectionUpdate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Update a section."""
    stmt = (
        select(CourseSection)
        .join(Course)
        .where(CourseSection.id == section_id, Course.tenant_id == current_user.tenant_id)
    )
    section = (await db.execute(stmt)).scalar_one_or_none()
    if not section:
        raise HTTPException(404, "Section not found")

    data = req.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(section, key, value)

    await db.commit()
    await db.refresh(section)

    count_stmt = select(func.count(Lesson.id)).where(Lesson.section_id == section.id)
    count = (await db.execute(count_stmt)).scalar() or 0

    return SectionResponse(**section.__dict__, lesson_count=count)


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: str,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    """Delete a section (cascades to lessons, quizzes, assignments)."""
    stmt = (
        select(CourseSection)
        .join(Course)
        .where(CourseSection.id == section_id, Course.tenant_id == current_user.tenant_id)
    )
    section = (await db.execute(stmt)).scalar_one_or_none()
    if not section:
        raise HTTPException(404, "Section not found")

    await db.delete(section)
    await db.commit()
    return None
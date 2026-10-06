"""VASTU ONE - LMS v2: Lesson Resources"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Course, CourseSection, Lesson, LessonResource


router = APIRouter(prefix="/api/lms/v2/resources", tags=["lms-v2-resources"])


class ResourceCreate(BaseModel):
    lesson_id: str
    title: str = Field(..., min_length=2, max_length=255)
    resource_type: str = "pdf"
    url: str = Field(..., min_length=5)
    size_kb: int = 0
    downloadable: bool = True
    order_index: int = 0


class ResourceResponse(BaseModel):
    id: str
    lesson_id: str
    title: str
    resource_type: str
    url: str
    size_kb: int
    downloadable: bool
    order_index: int
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    req: ResourceCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Lesson)
        .join(CourseSection, Lesson.section_id == CourseSection.id, isouter=True)
        .join(Course, CourseSection.course_id == Course.id, isouter=True)
    )
    # Simpler: just verify lesson exists
    lesson_stmt = select(Lesson).where(Lesson.id == req.lesson_id)
    if not (await db.execute(lesson_stmt)).scalar_one_or_none():
        raise HTTPException(404, "Lesson not found")
    
    resource = LessonResource(**req.model_dump())
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.get("/by-lesson/{lesson_id}", response_model=list[ResourceResponse])
async def list_resources(
    lesson_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(LessonResource).where(
        LessonResource.lesson_id == lesson_id
    ).order_by(LessonResource.order_index)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: str,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(LessonResource).where(LessonResource.id == resource_id)
    resource = (await db.execute(stmt)).scalar_one_or_none()
    if not resource:
        raise HTTPException(404, "Resource not found")
    await db.delete(resource)
    await db.commit()
    return None
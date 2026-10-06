"""
VASTU ONE - LMS v2: Lesson Detail API
========================================
Get single lesson with all metadata for course player.
"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from database.base import get_db
from database.models import (
    Course, CourseSection, Lesson, Enrollment, LessonProgress,
    LessonResource, DiscussionPost, LessonNote,
)


router = APIRouter(prefix="/api/lms/v2/player", tags=["lms-v2-player"])


class LessonDetailResponse(BaseModel):
    # Lesson info
    id: str
    title: str
    description: str | None
    content_type: str
    content_url: str | None
    text_content: str | None
    duration_minutes: int
    order_index: int
    is_preview: bool
    # Section + course
    section_id: str | None
    section_title: str | None
    course_id: str
    course_title: str
    # Progress
    is_completed: bool
    watch_seconds: int
    # Navigation
    prev_lesson_id: str | None
    next_lesson_id: str | None
    # Counts
    resources_count: int
    discussion_count: int
    notes_count: int


@router.get("/lesson/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson_detail(
    lesson_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get full lesson details for player."""
    # Get lesson
    lesson_stmt = select(Lesson).where(Lesson.id == lesson_id)
    lesson = (await db.execute(lesson_stmt)).scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    
    # Get section
    section = None
    if lesson.section_id:
        sec_stmt = select(CourseSection).where(CourseSection.id == lesson.section_id)
        section = (await db.execute(sec_stmt)).scalar_one_or_none()
    
    # Get course
    course = None
    if section:
        course_stmt = select(Course).where(Course.id == section.course_id)
        course = (await db.execute(course_stmt)).scalar_one_or_none()
    elif lesson.module_id:
        # Legacy: lesson under module
        from database.models import CourseModule
        mod_stmt = select(CourseModule).where(CourseModule.id == lesson.module_id)
        module = (await db.execute(mod_stmt)).scalar_one_or_none()
        if module:
            course_stmt = select(Course).where(Course.id == module.course_id)
            course = (await db.execute(course_stmt)).scalar_one_or_none()
    
    if not course:
        raise HTTPException(404, "Course not found for lesson")
    
    # Check enrollment
    enroll_stmt = select(Enrollment).where(
        Enrollment.course_id == course.id,
        Enrollment.student_id == current_user.id,
    )
    enrollment = (await db.execute(enroll_stmt)).scalar_one_or_none()
    
    is_completed = False
    watch_seconds = 0
    if enrollment:
        prog_stmt = select(LessonProgress).where(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.lesson_id == lesson_id,
        )
        progress = (await db.execute(prog_stmt)).scalar_one_or_none()
        if progress:
            is_completed = progress.is_completed
            watch_seconds = progress.watch_seconds
    
    # Navigation: prev/next lessons in same course
    # Get all lessons in course ordered
    all_lessons = []
    if section:
        section_ids_stmt = select(CourseSection.id).where(CourseSection.course_id == course.id)
        section_ids = [row[0] for row in (await db.execute(section_ids_stmt)).all()]
        if section_ids:
            lessons_stmt = select(Lesson).where(
                Lesson.section_id.in_(section_ids)
            ).order_by(Lesson.order_index)
            all_lessons = (await db.execute(lessons_stmt)).scalars().all()
    
    prev_id = None
    next_id = None
    for i, l in enumerate(all_lessons):
        if l.id == lesson_id:
            if i > 0:
                prev_id = all_lessons[i-1].id
            if i < len(all_lessons) - 1:
                next_id = all_lessons[i+1].id
            break
    
    # Count resources
    res_stmt = select(func.count(LessonResource.id)).where(LessonResource.lesson_id == lesson_id)
    resources_count = (await db.execute(res_stmt)).scalar() or 0
    
    # Count discussions
    disc_stmt = select(func.count(DiscussionPost.id)).where(DiscussionPost.lesson_id == lesson_id)
    discussion_count = (await db.execute(disc_stmt)).scalar() or 0
    
    # Count user notes
    notes_stmt = select(func.count(LessonNote.id)).where(
        LessonNote.lesson_id == lesson_id,
        LessonNote.student_id == current_user.id,
    )
    notes_count = (await db.execute(notes_stmt)).scalar() or 0
    
    return LessonDetailResponse(
        id=lesson.id,
        title=lesson.title,
        description=getattr(lesson, 'text_content', None),
        content_type=lesson.content_type,
        content_url=lesson.content_url,
        text_content=lesson.text_content,
        duration_minutes=lesson.duration_minutes,
        order_index=lesson.order_index,
        is_preview=lesson.is_preview,
        section_id=lesson.section_id,
        section_title=section.title if section else None,
        course_id=course.id,
        course_title=course.title,
        is_completed=is_completed,
        watch_seconds=watch_seconds,
        prev_lesson_id=prev_id,
        next_lesson_id=next_id,
        resources_count=resources_count,
        discussion_count=discussion_count,
        notes_count=notes_count,
    )


@router.get("/course/{course_id}/content")
async def get_course_content(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get full course content (sections + lessons with progress)."""
    # Get course
    course_stmt = select(Course).where(Course.id == course_id)
    course = (await db.execute(course_stmt)).scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found")
    
    # Get sections
    sec_stmt = select(CourseSection).where(CourseSection.course_id == course_id).order_by(CourseSection.order_index)
    sections = (await db.execute(sec_stmt)).scalars().all()
    
    # Get enrollment + progress
    enroll_stmt = select(Enrollment).where(
        Enrollment.course_id == course_id,
        Enrollment.student_id == current_user.id,
    )
    enrollment = (await db.execute(enroll_stmt)).scalar_one_or_none()
    
    completed_lesson_ids = set()
    if enrollment:
        prog_stmt = select(LessonProgress.lesson_id).where(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.is_completed == True,
        )
        completed_lesson_ids = {row[0] for row in (await db.execute(prog_stmt)).all()}
    
    # Build content tree
    content = []
    for section in sections:
        lessons_stmt = select(Lesson).where(Lesson.section_id == section.id).order_by(Lesson.order_index)
        lessons = (await db.execute(lessons_stmt)).scalars().all()
        
        content.append({
            "section_id": section.id,
            "section_title": section.title,
            "order_index": section.order_index,
            "lessons": [
                {
                    "id": l.id,
                    "title": l.title,
                    "duration_minutes": l.duration_minutes,
                    "content_type": l.content_type,
                    "is_preview": l.is_preview,
                    "is_completed": l.id in completed_lesson_ids,
                }
                for l in lessons
            ],
        })
    
    return {
        "course_id": course.id,
        "course_title": course.title,
        "course_description": course.description,
        "progress_pct": enrollment.progress_pct if enrollment else 0,
        "content": content,
    }
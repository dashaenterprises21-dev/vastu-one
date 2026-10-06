"""
VASTU ONE - LMS v2: Student Dashboard Stats
=============================================
Aggregated stats for student dashboard.
"""
from __future__ import annotations
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from database.base import get_db
from database.models import (
    Course, Enrollment, Lesson, LessonProgress, Certificate,
    Assignment, AssignmentSubmission, Quiz, QuizAttempt,
    StudentStreak, Achievement, CourseSection,
)


router = APIRouter(prefix="/api/lms/v2/dashboard", tags=["lms-v2-dashboard"])


@router.get("/stats")
async def get_student_stats(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated stats for student dashboard."""
    
    # Enrolled courses
    enrollments_stmt = select(Enrollment).where(
        Enrollment.student_id == current_user.id,
        Enrollment.is_active == True,
    )
    enrollments = (await db.execute(enrollments_stmt)).scalars().all()
    
    course_count = len(enrollments)
    
    # Completed lessons
    completed_stmt = select(func.count(LessonProgress.id)).where(
        LessonProgress.enrollment_id.in_([e.id for e in enrollments]) if enrollments else False,
        LessonProgress.is_completed == True,
    )
    if enrollments:
        completed_lessons = (await db.execute(completed_stmt)).scalar() or 0
    else:
        completed_lessons = 0
    
    # Total learning minutes
    total_minutes_stmt = select(func.sum(Lesson.duration_minutes)).join(
        LessonProgress, Lesson.id == LessonProgress.lesson_id
    ).where(
        LessonProgress.enrollment_id.in_([e.id for e in enrollments]) if enrollments else False,
        LessonProgress.is_completed == True,
    )
    if enrollments:
        total_minutes = (await db.execute(total_minutes_stmt)).scalar() or 0
    else:
        total_minutes = 0
    
    # Streak
    streak_stmt = select(StudentStreak).where(StudentStreak.student_id == current_user.id)
    streak = (await db.execute(streak_stmt)).scalar_one_or_none()
    
    # Achievements count
    ach_stmt = select(func.count(Achievement.id)).where(Achievement.student_id == current_user.id)
    achievements_count = (await db.execute(ach_stmt)).scalar() or 0
    
    # Certificates
    cert_stmt = select(func.count(Certificate.id)).join(
        Enrollment, Certificate.enrollment_id == Enrollment.id
    ).where(Enrollment.student_id == current_user.id)
    certificates = (await db.execute(cert_stmt)).scalar() or 0
    
    # Upcoming assignments
    enrolled_course_ids = [e.course_id for e in enrollments]
    upcoming_assignments = []
    if enrolled_course_ids:
        # Get sections in enrolled courses
        sections_stmt = select(CourseSection).where(CourseSection.course_id.in_(enrolled_course_ids))
        sections = (await db.execute(sections_stmt)).scalars().all()
        section_ids = [s.id for s in sections]
        
        if section_ids:
            # Assignments not yet submitted
            submitted_ids_stmt = select(AssignmentSubmission.assignment_id).where(
                AssignmentSubmission.student_id == current_user.id
            )
            submitted_ids = [row[0] for row in (await db.execute(submitted_ids_stmt)).all()]
            
            upcoming_stmt = select(Assignment).where(
                Assignment.section_id.in_(section_ids),
                Assignment.is_published == True,
                Assignment.id.notin_(submitted_ids) if submitted_ids else True,
            ).limit(5)
            upcoming_assignments = (await db.execute(upcoming_stmt)).scalars().all()
    
    return {
        "stats": {
            "total_courses": course_count,
            "completed_lessons": completed_lessons,
            "total_minutes": total_minutes,
            "current_streak": streak.current_streak_days if streak else 0,
            "longest_streak": streak.longest_streak_days if streak else 0,
            "achievements_count": achievements_count,
            "certificates_count": certificates,
        },
        "upcoming_assignments": [
            {
                "id": a.id,
                "title": a.title,
                "due_days": a.due_days,
                "max_score": a.max_score,
            }
            for a in upcoming_assignments[:3]
        ],
    }


@router.get("/continue-learning")
async def continue_learning(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get the next lesson to continue for each enrolled course."""
    enrollments_stmt = select(Enrollment).where(
        Enrollment.student_id == current_user.id,
        Enrollment.is_active == True,
    )
    enrollments = (await db.execute(enrollments_stmt)).scalars().all()
    
    result = []
    for enrollment in enrollments:
        # Get course
        course_stmt = select(Course).where(Course.id == enrollment.course_id)
        course = (await db.execute(course_stmt)).scalar_one_or_none()
        if not course:
            continue
        
        # Get all lessons in this course
        sections_stmt = select(CourseSection).where(CourseSection.course_id == course.id)
        sections = (await db.execute(sections_stmt)).scalars().all()
        section_ids = [s.id for s in sections]
        
        # Get lessons not yet completed
        completed_lesson_ids_stmt = select(LessonProgress.lesson_id).where(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.is_completed == True,
        )
        completed_ids = [row[0] for row in (await db.execute(completed_lesson_ids_stmt)).all()]
        
        next_lesson = None
        if section_ids:
            next_stmt = select(Lesson).where(
                Lesson.section_id.in_(section_ids),
                Lesson.id.notin_(completed_ids) if completed_ids else True,
            ).order_by(Lesson.order_index).limit(1)
            next_lesson = (await db.execute(next_stmt)).scalar_one_or_none()
        
        result.append({
            "course_id": course.id,
            "course_title": course.title,
            "progress_pct": enrollment.progress_pct,
            "next_lesson_id": next_lesson.id if next_lesson else None,
            "next_lesson_title": next_lesson.title if next_lesson else None,
            "next_lesson_duration": next_lesson.duration_minutes if next_lesson else 0,
            "resume_seconds": 0,
        })
    
    return {"courses": result}


@router.get("/achievements")
async def my_achievements(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Get all achievements (earned + locked)."""
    # Earned
    earned_stmt = select(Achievement).where(Achievement.student_id == current_user.id)
    earned = (await db.execute(earned_stmt)).scalars().all()
    
    # Available badge types
    available = [
        {"type": "first_lesson", "title": "First Steps", "icon": "🎯", "desc": "Complete your first lesson"},
        {"type": "streak_7", "title": "On Fire", "icon": "🔥", "desc": "7-day learning streak"},
        {"type": "streak_30", "title": "Unstoppable", "icon": "⚡", "desc": "30-day learning streak"},
        {"type": "course_complete", "title": "Graduate", "icon": "🎓", "desc": "Complete a full course"},
        {"type": "quiz_master", "title": "Quiz Master", "icon": "🏅", "desc": "Pass 10 quizzes"},
        {"type": "assignment_pro", "title": "Assignment Pro", "icon": "📝", "desc": "Submit 5 assignments"},
    ]
    
    earned_types = {a.badge_type for a in earned}
    
    return {
        "earned": [
            {"type": a.badge_type, "title": a.title, "icon": a.icon, "desc": a.description, "earned_at": a.earned_at}
            for a in earned
        ],
        "locked": [
            {**b, "unlocked": b["type"] in earned_types}
            for b in available
        ],
    }
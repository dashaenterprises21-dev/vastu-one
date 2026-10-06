"""VASTU ONE - LMS v2: Quizzes"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Course, CourseSection, Quiz, QuizQuestion, QuizAttempt


router = APIRouter(prefix="/api/lms/v2/quizzes", tags=["lms-v2-quizzes"])


class QuizCreate(BaseModel):
    section_id: str
    title: str
    description: str | None = None
    pass_percentage: int = 70
    time_limit_minutes: int = 0
    max_attempts: int = 3
    shuffle_questions: bool = False
    is_published: bool = False


class QuestionCreate(BaseModel):
    quiz_id: str
    question_text: str
    options: list[str]
    correct_option_index: int
    explanation: str | None = None
    points: int = 1
    order_index: int = 0


class AttemptSubmit(BaseModel):
    quiz_id: str
    answers: dict


class QuizResponse(BaseModel):
    id: str
    section_id: str
    title: str
    description: str | None
    pass_percentage: int
    max_attempts: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: str
    quiz_id: str
    question_text: str
    options: list
    points: int
    order_index: int

    class Config:
        from_attributes = True


class AttemptResponse(BaseModel):
    id: str
    quiz_id: str
    student_id: str
    score_percentage: float
    passed: bool
    started_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


@router.post("", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    req: QuizCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(CourseSection)
        .join(Course)
        .where(CourseSection.id == req.section_id, Course.tenant_id == current_user.tenant_id)
    )
    if not (await db.execute(stmt)).scalar_one_or_none():
        raise HTTPException(404, "Section not found")
    
    quiz = Quiz(**req.model_dump())
    db.add(quiz)
    await db.commit()
    await db.refresh(quiz)
    return quiz


@router.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def add_question(
    req: QuestionCreate,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    if req.correct_option_index >= len(req.options):
        raise HTTPException(400, "correct_option_index out of range")
    
    question = QuizQuestion(**req.model_dump())
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question


@router.get("/{quiz_id}/questions", response_model=list[QuestionResponse])
async def list_questions(
    quiz_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.order_index)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/attempt", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
async def submit_attempt(
    req: AttemptSubmit,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    quiz_stmt = select(Quiz).where(Quiz.id == req.quiz_id)
    quiz = (await db.execute(quiz_stmt)).scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    
    count_stmt = select(func.count(QuizAttempt.id)).where(
        QuizAttempt.quiz_id == req.quiz_id,
        QuizAttempt.student_id == current_user.id,
    )
    prev_count = (await db.execute(count_stmt)).scalar() or 0
    if prev_count >= quiz.max_attempts:
        raise HTTPException(400, f"Max attempts ({quiz.max_attempts}) reached")
    
    q_stmt = select(QuizQuestion).where(QuizQuestion.quiz_id == req.quiz_id)
    questions = (await db.execute(q_stmt)).scalars().all()
    
    total_points = sum(q.points for q in questions)
    earned = 0
    for q in questions:
        selected = req.answers.get(q.id)
        if selected is not None and int(selected) == q.correct_option_index:
            earned += q.points
    
    score = (earned / total_points * 100) if total_points > 0 else 0
    passed = score >= quiz.pass_percentage
    
    attempt = QuizAttempt(
        quiz_id=req.quiz_id,
        student_id=current_user.id,
        answers=req.answers,
        score_percentage=round(score, 2),
        passed=passed,
        completed_at=datetime.utcnow(),
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt


@router.get("/my-attempts", response_model=list[AttemptResponse])
async def my_attempts(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(QuizAttempt).where(QuizAttempt.student_id == current_user.id).order_by(QuizAttempt.started_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())
"""VASTU ONE - LMS v2: Assignments"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import Course, CourseSection, Assignment, AssignmentSubmission


router = APIRouter(prefix="/api/lms/v2/assignments", tags=["lms-v2-assignments"])


class AssignmentCreate(BaseModel):
    section_id: str
    title: str
    description: str
    due_days: int = 7
    max_score: int = 100
    attachment_url: str | None = None
    is_published: bool = False


class SubmissionCreate(BaseModel):
    assignment_id: str
    content_text: str | None = None
    file_url: str | None = None


class GradeRequest(BaseModel):
    score: float
    feedback: str | None = None


class AssignmentResponse(BaseModel):
    id: str
    section_id: str
    title: str
    description: str
    due_days: int
    max_score: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SubmissionResponse(BaseModel):
    id: str
    assignment_id: str
    student_id: str
    content_text: str | None
    file_url: str | None
    score: float | None
    feedback: str | None
    submitted_at: datetime
    graded_at: datetime | None

    class Config:
        from_attributes = True


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    req: AssignmentCreate,
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
    
    assignment = Assignment(**req.model_dump())
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment


@router.get("/by-section/{section_id}", response_model=list[AssignmentResponse])
async def list_assignments(
    section_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Assignment).where(Assignment.section_id == section_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_assignment(
    req: SubmissionCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    assignment_stmt = select(Assignment).where(Assignment.id == req.assignment_id)
    if not (await db.execute(assignment_stmt)).scalar_one_or_none():
        raise HTTPException(404, "Assignment not found")
    
    dup_stmt = select(AssignmentSubmission).where(
        AssignmentSubmission.assignment_id == req.assignment_id,
        AssignmentSubmission.student_id == current_user.id,
    )
    if (await db.execute(dup_stmt)).scalar_one_or_none():
        raise HTTPException(409, "Already submitted")
    
    submission = AssignmentSubmission(
        assignment_id=req.assignment_id,
        student_id=current_user.id,
        content_text=req.content_text,
        file_url=req.file_url,
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission


@router.get("/submissions/{assignment_id}", response_model=list[SubmissionResponse])
async def list_submissions(
    assignment_id: str,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AssignmentSubmission).where(AssignmentSubmission.assignment_id == assignment_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/submissions/{submission_id}/grade", response_model=SubmissionResponse)
async def grade_submission(
    submission_id: str,
    req: GradeRequest,
    current_user: RequireConsultant,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AssignmentSubmission).where(AssignmentSubmission.id == submission_id)
    submission = (await db.execute(stmt)).scalar_one_or_none()
    if not submission:
        raise HTTPException(404, "Submission not found")
    
    submission.score = req.score
    submission.feedback = req.feedback
    submission.graded_at = datetime.utcnow()
    await db.commit()
    await db.refresh(submission)
    return submission
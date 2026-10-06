"""VASTU ONE - LMS v2: Discussion + Notes + Bookmarks + Reviews"""
from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, RequireConsultant
from database.base import get_db
from database.models import DiscussionPost, LessonNote, LessonBookmark, CourseReview


router = APIRouter(prefix="/api/lms/v2/engagement", tags=["lms-v2-engagement"])


# ============ DISCUSSIONS ============
class PostCreate(BaseModel):
    lesson_id: str
    content: str
    parent_id: str | None = None


class PostResponse(BaseModel):
    id: str
    lesson_id: str
    user_id: str
    parent_id: str | None
    content: str
    upvotes: int
    is_instructor: bool
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/discussions", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    req: PostCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    post = DiscussionPost(
        lesson_id=req.lesson_id,
        user_id=current_user.id,
        parent_id=req.parent_id,
        content=req.content,
        is_instructor=(current_user.role.value == "CONSULTANT"),
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get("/discussions/{lesson_id}", response_model=list[PostResponse])
async def list_discussions(
    lesson_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(DiscussionPost).where(
        DiscussionPost.lesson_id == lesson_id,
        DiscussionPost.parent_id.is_(None),
    ).order_by(DiscussionPost.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.post("/discussions/{post_id}/upvote")
async def upvote_post(
    post_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(DiscussionPost).where(DiscussionPost.id == post_id)
    post = (await db.execute(stmt)).scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Post not found")
    post.upvotes += 1
    await db.commit()
    return {"upvotes": post.upvotes}


# ============ NOTES ============
class NoteCreate(BaseModel):
    lesson_id: str
    content: str
    timestamp_seconds: int = 0


class NoteResponse(BaseModel):
    id: str
    lesson_id: str
    student_id: str
    content: str
    timestamp_seconds: int
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    req: NoteCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    note = LessonNote(
        lesson_id=req.lesson_id,
        student_id=current_user.id,
        content=req.content,
        timestamp_seconds=req.timestamp_seconds,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


@router.get("/notes", response_model=list[NoteResponse])
async def my_notes(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(LessonNote).where(LessonNote.student_id == current_user.id).order_by(LessonNote.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(LessonNote).where(
        LessonNote.id == note_id,
        LessonNote.student_id == current_user.id,
    )
    note = (await db.execute(stmt)).scalar_one_or_none()
    if not note:
        raise HTTPException(404, "Note not found")
    await db.delete(note)
    await db.commit()
    return None


# ============ BOOKMARKS ============
class BookmarkCreate(BaseModel):
    lesson_id: str
    note: str | None = None
    timestamp_seconds: int = 0


@router.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    req: BookmarkCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    dup = await db.execute(select(LessonBookmark).where(
        LessonBookmark.lesson_id == req.lesson_id,
        LessonBookmark.student_id == current_user.id,
    ))
    if dup.scalar_one_or_none():
        raise HTTPException(409, "Already bookmarked")
    
    bookmark = LessonBookmark(
        lesson_id=req.lesson_id,
        student_id=current_user.id,
        note=req.note,
        timestamp_seconds=req.timestamp_seconds,
    )
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return {"id": bookmark.id, "message": "Bookmarked"}


@router.get("/bookmarks")
async def my_bookmarks(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(LessonBookmark).where(LessonBookmark.student_id == current_user.id)
    result = await db.execute(stmt)
    bookmarks = result.scalars().all()
    return [{"id": b.id, "lesson_id": b.lesson_id, "note": b.note, "created_at": b.created_at} for b in bookmarks]


@router.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookmark(
    bookmark_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(LessonBookmark).where(
        LessonBookmark.id == bookmark_id,
        LessonBookmark.student_id == current_user.id,
    )
    bookmark = (await db.execute(stmt)).scalar_one_or_none()
    if not bookmark:
        raise HTTPException(404, "Bookmark not found")
    await db.delete(bookmark)
    await db.commit()
    return None


# ============ REVIEWS ============
class ReviewCreate(BaseModel):
    course_id: str
    rating: int
    title: str | None = None
    review_text: str | None = None


@router.post("/reviews", status_code=status.HTTP_201_CREATED)
async def create_review(
    req: ReviewCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    if req.rating < 1 or req.rating > 5:
        raise HTTPException(400, "Rating must be 1-5")
    
    dup = await db.execute(select(CourseReview).where(
        CourseReview.course_id == req.course_id,
        CourseReview.student_id == current_user.id,
    ))
    if dup.scalar_one_or_none():
        raise HTTPException(409, "Already reviewed")
    
    review = CourseReview(
        course_id=req.course_id,
        student_id=current_user.id,
        rating=req.rating,
        title=req.title,
        review_text=req.review_text,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return {"id": review.id, "rating": review.rating, "message": "Review submitted"}


@router.get("/reviews/{course_id}")
async def list_reviews(
    course_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CourseReview).where(CourseReview.course_id == course_id).order_by(CourseReview.created_at.desc())
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    
    avg_stmt = select(func.avg(CourseReview.rating)).where(CourseReview.course_id == course_id)
    avg = (await db.execute(avg_stmt)).scalar() or 0
    
    return {
        "average_rating": round(float(avg), 2),
        "total_reviews": len(reviews),
        "reviews": [
            {"id": r.id, "rating": r.rating, "title": r.title, "review_text": r.review_text, "created_at": r.created_at}
            for r in reviews
        ],
    }
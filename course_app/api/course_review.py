from fastapi import HTTPException, Depends, APIRouter

from course_app.api.course import course_router
from course_app.db.models import CourseReview
from course_app.db.schema import  CourseReviewSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List




async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


course_review_router = APIRouter(prefix='/course_review', tags=['CourseReview'])


@course_review_router.post('/', response_model=dict)
async def create_review(review: CourseReviewSchema, db: Session = Depends(get_db)):
    course_review = CourseReview(**review.dict())
    db.add(course_review)
    db.commit()
    db.refresh(course_review)
    return {'message': 'Saved'}


@course_review_router.delete('/{course_id}')
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(CourseReview).filter(CourseReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Course_review Deleted')

    db.add(review_db)
    db.commit()
    return {'message': 'Deleted'}
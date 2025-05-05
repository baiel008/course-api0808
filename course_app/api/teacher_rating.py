from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import TeacherRating
from course_app.db.schema import  TeacherRatingSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


rating_router = APIRouter(prefix='/teacher_rating', tags=['TeacherRating'])


@rating_router.post('/', response_model=dict)
async def create_rating(review: TeacherRatingSchema, db: Session = Depends(get_db)):
    rating = TeacherRating(**review.dict())
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return {'message': 'Saved'}


@rating_router.delete('/{rating_id}')
async def rating_delete(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(TeacherRating).filter(TeacherRating.id == rating_id).first()
    if rating_db is None:
        raise HTTPException(status_code=404, detail='Rating not Deleted')

    db.add(rating_db)
    db.commit()
    return {'message': 'Deleted'}
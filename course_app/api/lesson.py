from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import Network, Lesson
from course_app.db.schema import NetworkSchema, NetworkCreateSchema, LessonCreateSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

lesson_router = APIRouter(prefix='/lesson', tags=['Lesson'])

@lesson_router.post('/', response_model=dict)
async def create_lesson(lesson: LessonCreateSchema, db: Session = Depends(get_db)):
    lesson_db = Lesson(**lesson.dict())
    db.add(lesson_db)
    db.commit()
    db.refresh(lesson_db)
    return {'message': 'Saved'}


@lesson_router.delete('/{lesson_id}')
async def lesson_delete(lesson_id: int, db: Session = Depends(get_db)):
    lesson_db = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson_db is None:
        raise HTTPException(status_code=404, detail='Course Deleted')

    db.add(lesson_db)
    db.commit()
    return {'message': 'Deleted'}
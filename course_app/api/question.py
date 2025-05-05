from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import  Questions
from course_app.db.schema import QuestionSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

questions_router = APIRouter(prefix='/questions', tags=['Questions'])



@questions_router.post('/', response_model=dict)
async def questions_create(questions: QuestionSchema, db: Session = Depends(get_db)):
    questions_db = Questions(**questions.dict())
    db.add(questions_db)
    db.commit()
    db.refresh(questions_db)
    return {'message': 'Saved'}


@questions_router.delete('/{questions_id}')
async def questions_delete(questions: int, db: Session = Depends(get_db)):
    questions_db = db.query(Questions).filter(Questions.id == questions).first()
    if questions_db is None:
        raise HTTPException(status_code=404, detail='not questions Deleted')
    db.add(questions_db)
    db.commit()
    return {'message': 'Deleted'}
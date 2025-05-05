from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import Assignment
from course_app.db.schema import AssignmentSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List



async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


assignment_router = APIRouter(prefix='/assignment', tags=['Assignment'])


@assignment_router.post('/', response_model=dict)
async def assignment_create(assignment: AssignmentSchema, db: Session = Depends(get_db)):
    assignment_db = Assignment(**assignment.dict())
    db.add(assignment_db)
    db.commit()
    db.refresh(assignment_db)
    return {'message': 'Saved'}


@assignment_router.delete('/{assignment_id}')
async def assignment_delete(assignment_id: int, db: Session = Depends(get_db)):
    assignment_db = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if assignment_db is None:
        raise HTTPException(status_code=404, detail='Course Deleted')

    db.add(assignment_db)
    db.commit()
    return {'message': 'Deleted'}
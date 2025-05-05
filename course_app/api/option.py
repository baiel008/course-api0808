from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import  Option
from course_app.db.schema import OptionSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

option_router = APIRouter(prefix='/option', tags=['Option'])



@option_router.post('/', response_model=dict)
async def option_create(history: OptionSchema, db: Session = Depends(get_db)):
    option_db = Option(**history.dict())
    db.add(option_db)
    db.commit()
    db.refresh(option_db)
    return {'message': 'Saved'}


@option_router.delete('/{option_id}')
async def option_delete(history_id: int, db: Session = Depends(get_db)):
    option_db = db.query(Option).filter(Option.id == history_id).first()
    if option_db is None:
        raise HTTPException(status_code=404, detail='option not Deleted')

    db.add(option_db)
    db.commit()
    return {'message': 'Deleted'}
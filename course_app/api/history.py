from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import History
from course_app.db.schema import HistorySchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

history_router = APIRouter(prefix='/history', tags=['History'])



@history_router.post('/', response_model=dict)
async def history_create(history: HistorySchema, db: Session = Depends(get_db)):
    history_db = History(**history.dict())
    db.add(history_db)
    db.commit()
    db.refresh(history_db)
    return {'message': 'Saved'}


@history_router.delete('/{history_id}')
async def history_delete(history_id: int, db: Session = Depends(get_db)):
    history_db = db.query(History).filter(History.id == history_id).first()
    if history_db is None:
        raise HTTPException(status_code=404, detail='history not Deleted')

    db.add(history_db)
    db.commit()
    return {'message': 'Deleted'}
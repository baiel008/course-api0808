from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import Network
from course_app.db.schema import NetworkSchema, NetworkCreateSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

network_router = APIRouter(prefix='/network', tags=['Network'])

@network_router.post('/', response_model=dict)
async def create_network(network: NetworkCreateSchema, db: Session = Depends(get_db)):
    network_db = Network(**network.dict())
    db.add(network_db)
    db.commit()
    db.refresh(network_db)
    return {'message': 'Saved'}


@network_router.delete('/{network_id}')
async def network_delete(network_id: int, db: Session = Depends(get_db)):
    network_db = db.query(Network).filter(Network.id == network_id).first()
    if network_db is None:
        raise HTTPException(status_code=404, detail='Network Deleted')

    db.add(network_db)
    db.commit()
    return {'message': 'Deleted'}

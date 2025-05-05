from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import Certificates
from course_app.db.schema import  CertificateSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


certificate_router = APIRouter(prefix='/certificate', tags=['Certificate'])


@certificate_router.post('/', response_model=dict)
async def create_certificate(certificate: CertificateSchema, db: Session = Depends(get_db)):
    certificate_db = Certificates(**certificate.dict())
    db.add(certificate_db)
    db.commit()
    db.refresh(certificate_db)
    return {'message': 'Saved'}


@certificate_router.delete('/{certificate_id}')
async def certificate_delete(certificate_id: int, db: Session = Depends(get_db)):
    certificate_db = db.query(Certificates).filter(Certificates.id == certificate_id).first()
    if certificate_db is None:
        raise HTTPException(status_code=404, detail='Course Deleted')

    db.add(certificate_db)
    db.commit()
    return {'message': 'Deleted'}




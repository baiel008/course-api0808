from fastapi import HTTPException, Depends, APIRouter, Query
from course_app.db.models import Course, StatusChoices, TypeChoices
from course_app.db.schema import CourseCreateSchema, CourseOutSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List, Optional



async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


course_router = APIRouter(prefix='/course', tags=['Course'])


@course_router.post('/', response_model=dict)
async def course_create(course: CourseCreateSchema, db: Session = Depends(get_db)):
    course_db = Course(**course.dict())
    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return {'message': 'Saved'}



@course_router.get('/search/', response_model=List[CourseOutSchema])
async def search_course(course_name: str, db: Session =Depends(get_db)):
    course_db = db.query(Course).filter(Course.course_name.ilike(f'%{course_name}%')).all()
    if not course_db:
        raise HTTPException(status_code=404, detail='Course not found')
    return course_db


@course_router.get('/', response_model=List[CourseOutSchema])
async def course_list(min_price: Optional[float] = Query(None, alias='price[from]'),
                      max_price: Optional[float] =  Query(None, alias='price[to]'),
                      level: Optional[StatusChoices] = None,
                      type_course: Optional[TypeChoices] = None,
                      db: Session =Depends(get_db)):


    query = db.query(Course)

    if min_price is not  None:
        query = query.filter(Course.price >= min_price)

    if max_price is not None:
        query = query.filter(Course.price <= max_price)

    if level:
        query = query.filter(Course.level == level)

    if type_course:
        query = query.filter(Course.type == type_course)

    courses = query.all()

    if not courses:
        raise HTTPException(status_code=404, detail='Course not found')

    return courses



@course_router.get('/{course_id}', response_model=List[CourseOutSchema])
async def course_detail(course_id: int, db: Session =Depends(get_db)):
    course_db = db.query(Course).filter(Course.id == course_id).first()
    if not course_db:
        raise HTTPException(status_code=404, detail='Course not found')
    return [course_db]


@course_router.put('/', response_model=CourseOutSchema)
async def course_update(course_id: int, course: CourseCreateSchema,
                        db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.id == course_id).first()
    if not course_db:
        raise HTTPException(status_code=404, detail='Course not found')

    for course_key, course_value, in course.dict().items():
        setattr(course_db, course_key, course_value)

    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return course_db

@course_router.delete('/{course_id}')
async def course_delete(course_id: int, db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.id == course_id).first()
    if course_db is None:
        raise HTTPException(status_code=404, detail='Course Deleted')

    db.add(course_db)
    db.commit()
    return {'message': 'Deleted'}
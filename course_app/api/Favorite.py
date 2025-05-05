from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import Favorite, FavoriteItem, Course
from course_app.db.schema import FavoriteSchema, FavoriteItemSchema, FavoriteItemCreateSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List



async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


favorite_router = APIRouter(prefix='/favorite', tags=['Favorite'])


@favorite_router.get('/', response_model=FavoriteSchema)
async def favorite_list(user_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail='Favorite not found')
    return favorite


@favorite_router.post('/', response_model=FavoriteItemSchema)
async def favorite_add(item_data: FavoriteItemCreateSchema, user_id: int,
                       db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite:
        favorite = Favorite(user_id=user_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)

    course = db.query(Course).filter(Course.id == item_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail='Course Not Found')

    course_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite.id,
                                             FavoriteItem.course_id == item_data.course_id).first()

    if course_item:
        raise HTTPException(status_code=404, detail='Course saved')

    favorite_item = FavoriteItem(favorite_id=favorite.id, course_id=item_data.course_id)
    db.add(favorite_item)
    db.commit()
    db.refresh(favorite_item)

    return favorite_item

@favorite_router.delete('/')
async def favorite_delete(course_id: int, user_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail='Избранные не найдена')

    fav_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite.id,
                                             FavoriteItem.course_id == course_id).first()

    if not fav_item:
        raise HTTPException(status_code=404, detail='Избранные отсуствует в корзине')

    db.delete(fav_item)
    db.commit()
    return {'message': 'Продукт удален из избранных'}
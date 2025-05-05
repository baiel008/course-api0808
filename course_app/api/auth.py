from fastapi import HTTPException, Depends, APIRouter
from course_app.db.models import UserProfile, RefreshToken, Cart, Favorite
from course_app.db.schema import UserProfileSchema, UserProfileLoginSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from course_app.config import (ALGORITHM, SECRET_KEYS,
                              ACCESS_TOKEN_LIFETIME,
                              REFRESH_TOKEN_LIFETIME)
from datetime import timedelta, datetime

async def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
auth_router = APIRouter(prefix='/auth', tags=['Auth'])



def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEYS, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register/')
async def register(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    user_email = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail='username is already taken')
    elif user_email:
        raise HTTPException(status_code=400, detail='есть')
    new_hash_pass = get_password_hash(user.password)
    new_user = UserProfile(
        age=user.age,
        phone_number=user.phone_number,
        profile_picture=user.profile_picture,
        bio_teacher=user.bio_teacher,
        days=user.days,
        status=user.status,
        subject=user.subject,
        experience=user.experience,
        role=user.role,
        password=new_hash_pass,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_cart = Cart(user_id=new_user.id)
    db.add(new_cart)
    db.commit()

    new_fav = Favorite(user_id=new_user.id)
    db.add(new_fav)
    db.commit()
    return {'message': 'Saved'}


@auth_router.post('/login')
async def login(form_data: UserProfileLoginSchema = Depends(),
                db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
         raise HTTPException(status_code=404, detail='Маалымат туура эмес')

    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})

    new_token = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(new_token)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'type_token': 'bearer'}


@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):

    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=404, detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()

    return {'message': 'Вышли'}


@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=404, detail='Маалымат туура эмес')

    access_token = create_access_token({'sub': stored_token.id})

    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.delete('/')
async def delete_users(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='Not Users')
    db.delete(user_db)
    db.commit()
    return {'message': 'Deleted'}
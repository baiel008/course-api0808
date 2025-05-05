from fastapi import APIRouter
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from authlib.integrations.starlette_client import OAuth
from course_app.config import settings
from starlette.requests import Request



social_router = APIRouter(prefix='/oauth', tags=['Social Pauth'])


oauth = OAuth()
oauth.register(
    name = 'github',
    client_id = settings.GITHUB_CLIENT_ID,
    secret_key = settings.GITHUB_SECRET,
    authorize_url='https://github.com/login/oauth/authorize',
)

oauth.register(
    name = 'google',
    client_id = settings.GOOGLE_CLIENT_ID,
    secret_key = settings.GOOGLE_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile email"},
)


@social_router.get('/github')
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_URL
    return await oauth.github.authorize_redirect(request, redirect_uri)

@social_router.get('/google')
async def accounts_login_callback(request: Request):
    redirect_uri = settings.GOOGLE_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEYS = os.getenv('SECRET_KEYS')
ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME = 30
REFRESH_TOKEN_LIFETIME = 3


class Settings:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_SECRET = os.getenv('GITHUB_SECRET')
    GITHUB_URL = os.getenv('GITHUB_URL')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET = os.getenv('GOOGLE_SECRET')
    GOOGLE_URL = os.getenv('GOOGLE_URL')


settings = Settings
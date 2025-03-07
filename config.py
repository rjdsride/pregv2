from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "mykey"
    SESSION_COOKIE_NAME: str = "session_token"
    SESSION_EXPIRE_MINUTES: int = 1440

settings = Settings()

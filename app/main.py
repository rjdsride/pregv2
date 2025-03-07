from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from app.routes import auth_router, home_router, service_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE_NAME,
    max_age=settings.SESSION_EXPIRE_MINUTES * 60
)

app.include_router(home_router.router)
app.include_router(auth_router.router)
app.include_router(service_router.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


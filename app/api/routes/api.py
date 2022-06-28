from fastapi import APIRouter

from app.api.routes import sessions

router = APIRouter()

router.include_router(sessions.router, tags=["sessions"], prefix="/sessions")

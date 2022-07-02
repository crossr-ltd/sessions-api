from fastapi import APIRouter

from app.api.routes import sessions
from app.api.routes import datasets

router = APIRouter()

router.include_router(sessions.router, tags=["sessions"], prefix="/sessions")
router.include_router(datasets.router, tags=["datasets"], prefix="/datasets")

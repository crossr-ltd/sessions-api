from fastapi import APIRouter, Request

from app.api.services.sessions import get_session

router = APIRouter()


@router.get("/session/{id}")
async def session_get(request: Request, id: str):
    return get_session(id)
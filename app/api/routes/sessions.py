from fastapi import APIRouter, Request

from app.api.models.schemas import SessionUpdateParams
from app.api.services.sessions import get_session, update_session

router = APIRouter()


@router.get("/{id}")
async def session_get(request: Request, id: str):
    return get_session(id)


@router.post("/update")
async def session_update(request: Request, session_update_params: SessionUpdateParams):
    return update_session(**dict(session_update_params))

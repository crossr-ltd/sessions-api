from fastapi import APIRouter, Request

from app.api.models.schemas import SessionUpdateParams, SessionCreateParams
from app.api.services.sessions import get_session, update_session, get_all_sessions, create_session, delete_session

router = APIRouter()


@router.get("/{id}")
async def session_get(request: Request, id: str):
    return get_session(id)


@router.post("/update")
async def session_update(request: Request, session_update_params: SessionUpdateParams):
    return update_session(**dict(session_update_params))


@router.get('/{id}/delete')
async def session_delete(request: Request, id: str):
    return delete_session(id)


@router.get("/")
async def session_get_all(request: Request):
    return get_all_sessions()


@router.post("/create")
async def session_create(request: Request, session_create_params: SessionCreateParams):
    return create_session(**dict(session_create_params))

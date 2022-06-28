from pydantic import BaseModel

from app.api.models.domains import Session


class SessionUpdateParams(BaseModel):
    session: Session

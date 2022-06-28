from typing import Optional

from fastapi import HTTPException, Request, Depends, Header
from jwt import decode


def pseudo_validate_locally(token):
    return decode(token, options={"verify_signature": False}, algorithms=["RS256"])


def get_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(403, "Missing 'Authorization' header.")
    try:
        return authorization.split()[1]
    except IndexError:
        raise HTTPException(403, "Malformed 'Authorization' header.")


def current_user(
        request: Request, token: str = Depends(get_token)
):
    """function to authenticate the user via auth0, and store user_id for database queries."""
    try:
        user_metadata = pseudo_validate_locally(token)
        request.state.user_id = user_metadata['sub']
    except Exception as e:
        raise HTTPException(403, str(e))

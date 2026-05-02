from fastapi import APIRouter, Depends, Request, Response
from sqlmodel import Session

from app.db import get_session
from app.enums.api_status import APIStatus
from app.schemas.response.api_response import APIResponse
from app.services import game_service, session_service

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/newgame", response_model=APIResponse)
def new_game(
    request: Request, response: Response, session: Session = Depends(get_session)
):
    ua = request.headers.get("user-agent", "unknown")

    # New game logic
    try:
        result = game_service.create_new_game(ua, session)
    except ValueError as e:
        # Temporarily log to the server's console
        print(e)

        return APIResponse(
            status=APIStatus.ERROR,
            message="Server error while creating new game",
            code=500,
        )

    # Create session token
    session_token = session_service.create_token(result.game_id, ua)

    # Store session token in cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,  # HTTPS only
        samesite="strict",  # CSRF protection
        max_age=1800,  # 30 min, matches JWT expiry
    )
    return APIResponse(status=APIStatus.SUCCESS, data=result, code=200)

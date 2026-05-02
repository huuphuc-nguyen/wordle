from fastapi import APIRouter, Request, Response

from app.enums.api_status import APIStatus
from app.schemas.response.api_response import APIResponse
from app.services import game_service, session_service

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/newgame", response_model=APIResponse)
def new_game(request: Request, response: Response):
    ua = request.headers.get("user-agent", "unknown")

    # Create new game ID
    result = game_service.create_new_game()

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
    return APIResponse(status=APIStatus.SUCCESS, data=result)

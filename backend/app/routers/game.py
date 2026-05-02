from fastapi import APIRouter, Depends, Request, Response
from sqlmodel import Session

from app.db import get_session
from app.enums.api_status import APIStatus
from app.schemas.request.guess_request import GuessRequest
from app.schemas.response.api_response import APIResponse
from app.services import game_service, session_service

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/newgame", response_model=APIResponse)
def new_game(
    request: Request, response: Response, session: Session = Depends(get_session)
):

    # New game logic
    try:
        result = game_service.create_new_game(session)
    except ValueError as e:
        # Temporarily log to the server's console
        print(e)

        return APIResponse(
            status=APIStatus.ERROR,
            message="Server error while creating new game",
            code=500,
        )

    # Create session token
    session_token = session_service.create_token(result.game_id)

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


@router.post("/guess", response_model=APIResponse)
def guess(
    request: Request, body: GuessRequest, session: Session = Depends(get_session)
):
    token = request.cookies.get("session_token")

    game_id = session_service.get_game_id_from_token(token)

    # Validate token
    # 401 when: token is missing or expired, token is invalid, fail to decode and get game_id
    if not session_service.verify_token(token, game_id):
        return APIResponse(
            status=APIStatus.ERROR, message="Invalid or expired session", code=401
        )

    try:
        assert game_id is not None  # already check in verify_token
        result = game_service.submit_guess(game_id, body, session)
    except ValueError as e:
        return APIResponse(status=APIStatus.ERROR, message=str(e), code=400)

    return APIResponse(status=APIStatus.SUCCESS, data=result, code=200)

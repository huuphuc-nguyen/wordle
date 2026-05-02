"""Game routes — handles new game creation and guess submission."""

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
    """Start a new game — picks a random word, saves the game, sets a session cookie."""

    try:
        result = game_service.create_new_game(session)
    except ValueError as e:
        # Word table is empty or DB error
        print(e)
        return APIResponse(
            status=APIStatus.ERROR,
            message="Server error while creating new game",
            code=500,
        )

    # Sign a JWT with the game_id and store it as an HttpOnly cookie
    # Frontend never sees or manages this token directly
    session_token = session_service.create_token(result.game_id)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,  # JS cannot read this cookie
        secure=True,  # HTTPS only
        samesite="strict",
        max_age=1800,  # 30 min, matches JWT expiry
    )
    return APIResponse(status=APIStatus.SUCCESS, data=result, code=200)


@router.post("/guess", response_model=APIResponse)
def guess(
    request: Request, body: GuessRequest, session: Session = Depends(get_session)
):
    """Submit a guess — verifies the session cookie, scores the word, returns the result."""

    # Read the session cookie set by /newgame
    token = request.cookies.get("session_token")

    # Decode the game_id from the token without trusting the client to send it
    game_id = session_service.get_game_id_from_token(token)

    # 401 when: token is missing, expired, tampered
    if game_id is None:
        return APIResponse(
            status=APIStatus.ERROR, message="Invalid or expired session", code=401
        )

    try:
        result = game_service.submit_guess(game_id, body, session)
    except ValueError as e:
        # Invalid word, game not found, or game already over
        return APIResponse(status=APIStatus.ERROR, message=str(e), code=400)

    return APIResponse(status=APIStatus.SUCCESS, data=result, code=200)

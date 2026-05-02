from fastapi import APIRouter

from app.enums.api_status import APIStatus
from app.schemas.response.api_response import APIResponse
from app.services import game_service

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/newgame", response_model=APIResponse)
def new_game():
    result = game_service.create_new_game()
    return APIResponse(status=APIStatus.SUCCESS, data=result)

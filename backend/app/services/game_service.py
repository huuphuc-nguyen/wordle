import uuid

from app.schemas.response.newgame_response import NewGameResponse


def create_new_game() -> NewGameResponse:
    return NewGameResponse(game_id=str(uuid.uuid4()), session_token=str(uuid.uuid4()))

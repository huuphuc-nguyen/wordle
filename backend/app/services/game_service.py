import uuid

from app.schemas.response.newgame_response import NewGameResponse


def create_new_game() -> NewGameResponse:
    game_id = str(uuid.uuid4())
    return NewGameResponse(game_id=game_id)

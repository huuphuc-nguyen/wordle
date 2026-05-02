from pydantic import BaseModel


class NewGameResponse(BaseModel):
    game_id: str

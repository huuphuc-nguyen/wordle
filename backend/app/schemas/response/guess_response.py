from typing import Dict, List

from pydantic import BaseModel

from app.enums.game_status import GameStatus


class GuessResponse(BaseModel):
    score: List[str]
    attempts: int
    status: GameStatus
    keyboard: Dict[str, str]

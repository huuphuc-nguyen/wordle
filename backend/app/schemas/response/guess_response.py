"""GuessResponse — result of a single guess submission."""

from typing import Dict, List

from pydantic import BaseModel

from app.enums.game_status import GameStatus


class GuessResponse(BaseModel):
    # Per-letter result for this guess: "correct", "present", or "absent"
    score: List[str]

    # Total guesses submitted so far (including this one)
    attempts: int

    # Current game state after this guess
    status: GameStatus

    # Best known state for all 26 letters across all guesses — used to colour the keyboard on the frontend
    keyboard: Dict[str, str]

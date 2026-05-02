"""GuessRequest — validates the word submitted by the player."""

from pydantic import BaseModel


class GuessRequest(BaseModel):
    # The player's guessed word — must be exactly 5 letters (validated here before hitting the service)
    word: str

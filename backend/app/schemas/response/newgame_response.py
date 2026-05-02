"""NewGameResponse — returned after a new game is created."""

from pydantic import BaseModel


class NewGameResponse(BaseModel):
    # The game identifier — sent to the frontend so it knows which game it's playing
    # The session token (stored in cookie) ties this game_id to the user's session
    game_id: str

"""Session service — create and verify JWT session tokens stored in cookies."""

import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRY_MINUTES = 30


def create_token(game_id: str) -> str:
    """Sign a JWT containing the game_id, expires in 30 minutes."""
    payload = {
        "game_id": game_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_MINUTES),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str | None, game_id: str | None) -> bool:
    """Return True if the token is valid, not expired, and matches the given game_id."""
    if not token or not game_id:
        return False

    try:
        # jwt.decode automatically rejects expired tokens
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["game_id"] == game_id
    except jwt.PyJWTError:
        return False


def get_game_id_from_token(token: str | None) -> str | None:
    """Decode the token and return the game_id, or None if invalid or expired."""
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["game_id"]
    except jwt.PyJWTError:
        return None

import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRY_MINUTES = 30


def create_token(game_id: str) -> str:
    payload = {
        "game_id": game_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_MINUTES),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str | None, game_id: str | None) -> bool:
    if not token or not game_id:
        return False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["game_id"] == game_id
    except jwt.PyJWTError:
        return False


def get_game_id_from_token(token: str | None) -> str | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["game_id"]
    except jwt.PyJWTError:
        return None

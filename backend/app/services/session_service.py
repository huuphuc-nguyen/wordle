import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRY_MINUTES = 30


def create_token(game_id: str, ua: str) -> str:
    payload = {
        "game_id": game_id,
        "ua": ua,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_MINUTES),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str, game_id: str, ua: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["game_id"] == game_id and payload["ua"] == ua
    except jwt.PyJWTError:
        return False

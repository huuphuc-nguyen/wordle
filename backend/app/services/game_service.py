import uuid

from sqlmodel import Session, func, select

from app.models.word import Word
from app.schemas.response.newgame_response import NewGameResponse


def get_random_word(session: Session) -> str:
    word = session.exec(select(Word).order_by(func.random()).limit(1)).first()
    if not word:
        raise ValueError("No words in database")
    return word.word


def create_new_game(ua: str, session: Session) -> NewGameResponse:
    game_id = str(uuid.uuid4())
    secret_word = get_random_word(session)
    print(f"[game {game_id}] secret word: {secret_word}")
    return NewGameResponse(game_id=game_id)

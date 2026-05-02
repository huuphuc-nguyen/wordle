from sqlmodel import Session, func, select

from app.models.game import Game
from app.models.word import Word
from app.schemas.response.newgame_response import NewGameResponse


def _get_random_word(session: Session) -> str:
    word = session.exec(select(Word).order_by(func.random()).limit(1)).first()
    if not word:
        raise ValueError("No words in database")
    return word.word


def create_new_game(session: Session) -> NewGameResponse:
    secret_word = _get_random_word(session)
    game = Game(secret_word=secret_word, guesses=[], attempts=0)
    session.add(game)
    session.commit()
    session.refresh(game)
    return NewGameResponse(game_id=game.uuid)

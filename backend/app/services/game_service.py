from sqlmodel import Session, func, select

from app.enums.game_status import GameStatus
from app.models.game import Game
from app.models.word import Word
from app.schemas.request.guess_request import GuessRequest
from app.schemas.response.guess_response import GuessResponse
from app.schemas.response.newgame_response import NewGameResponse


def _get_random_word(session: Session) -> str:
    word = session.exec(select(Word).order_by(func.random()).limit(1)).first()
    if not word:
        raise ValueError("No words in database")
    return word.word


def create_new_game(session: Session) -> NewGameResponse:
    secret_word = _get_random_word(session)
    game = Game(secret_word=secret_word, guesses=[], attempts=0)
    print(secret_word)
    session.add(game)
    session.commit()
    session.refresh(game)
    return NewGameResponse(game_id=game.uuid)


def submit_guess(game_id: str, body: GuessRequest, session: Session):
    game = session.exec(
        select(Game).where(Game.uuid == game_id, Game.status == GameStatus.ACTIVE)
    ).first()
    if not game:
        raise ValueError("Game not found or already over")

    guess = body.word
    is_valid_word = session.exec(select(Word).where(Word.word == guess)).first()
    if not is_valid_word:
        raise ValueError("Not a valid word")

    score = _score_guess(guess, game.secret_word)

    game.guesses = game.guesses + [guess]
    game.attempts += 1

    if guess == game.secret_word:
        game.status = GameStatus.WON
    elif game.attempts >= 6:
        game.status = GameStatus.LOST

    session.add(game)
    session.commit()
    session.refresh(game)

    keyboard = _build_keyboard(game.guesses, game.secret_word)

    return GuessResponse(
        score=score, attempts=game.attempts, status=game.status, keyboard=keyboard
    )


PRIORITY = {"correct": 3, "present": 2, "absent": 1, "unknown": 0}


def _build_keyboard(guesses: list[str], secret: str) -> dict[str, str]:
    keyboard = {chr(i): "unknown" for i in range(ord("a"), ord("z") + 1)}
    for guess in guesses:
        for letter, state in zip(guess, _score_guess(guess, secret)):
            if PRIORITY[state] > PRIORITY[keyboard[letter]]:
                keyboard[letter] = state
    return keyboard


def _score_guess(guess: str, secret: str) -> list[str]:
    score = ["absent"] * 5
    pool = list(secret)

    for i, letter in enumerate(guess):
        if letter == secret[i]:
            score[i] = "correct"
            pool.remove(letter)

    for i, letter in enumerate(guess):
        if score[i] == "correct":
            continue
        if letter in pool:
            score[i] = "present"
            pool.remove(letter)

    return score

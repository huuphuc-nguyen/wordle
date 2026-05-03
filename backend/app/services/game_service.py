"""Game service — core game logic: create games, score guesses, build keyboard state."""

from sqlmodel import Session, func, select

from app.enums.game_status import GameStatus
from app.models.game import Game
from app.models.word import Word
from app.schemas.request.guess_request import GuessRequest
from app.schemas.response.guess_response import GuessResponse
from app.schemas.response.newgame_response import NewGameResponse

# Priority order for keyboard state — a letter never downgrades to a lower state
PRIORITY = {"correct": 3, "present": 2, "absent": 1, "unknown": 0}


def get_secret_word(game_id: str, session: Session) -> dict:
    """Return the secret word only if the game is finished (won or lost)."""
    game = session.exec(
        select(Game).where(Game.uuid == game_id, Game.status != GameStatus.ACTIVE)
    ).first()
    if not game:
        raise ValueError("Game not found or still in progress")
    return {"secret_word": game.secret_word}


def _get_random_word(session: Session) -> str:
    """Pick one random word from the word table."""
    word = session.exec(select(Word).order_by(func.random()).limit(1)).first()
    if not word:
        raise ValueError("No words in database")
    return word.word


def create_new_game(session: Session) -> NewGameResponse:
    """Create a new game row with a random secret word and return the game_id."""
    secret_word = _get_random_word(session)
    game = Game(secret_word=secret_word, guesses=[], attempts=0)
    print(secret_word)  # temporary — remove before production
    session.add(game)
    session.commit()
    session.refresh(game)
    return NewGameResponse(game_id=game.uuid)


def submit_guess(game_id: str, body: GuessRequest, session: Session) -> GuessResponse:
    """
    Process a guess for the given game.

    Raises ValueError if:
    - game not found or not active
    - guess is not in the word list
    """
    # Only fetch games that are still active — finished games are rejected here
    game = session.exec(
        select(Game).where(Game.uuid == game_id, Game.status == GameStatus.ACTIVE)
    ).first()
    if not game:
        raise ValueError("Game not found or already over")

    guess = body.word

    # Reject guesses that aren't real words in the word list
    is_valid_word = session.exec(select(Word).where(Word.word == guess)).first()
    if not is_valid_word:
        raise ValueError("Not a valid word")

    score = _score_guess(guess, game.secret_word)

    # Append guess and increment attempts — reassign list so SQLAlchemy tracks the change
    game.guesses = game.guesses + [guess]
    game.attempts += 1

    # Update game status if the player won or used all 6 attempts
    if guess == game.secret_word:
        game.status = GameStatus.WON
    elif game.attempts >= 6:
        game.status = GameStatus.LOST

    session.add(game)
    session.commit()
    session.refresh(game)

    # Build the full keyboard state across all guesses so the frontend can colour the keys
    keyboard = _build_keyboard(game.guesses, game.secret_word)

    return GuessResponse(
        score=score, attempts=game.attempts, status=game.status, keyboard=keyboard
    )


def _build_keyboard(guesses: list[str], secret: str) -> dict[str, str]:
    """Return the best known state for each letter across all guesses so far."""
    keyboard = {chr(i): "unknown" for i in range(ord("a"), ord("z") + 1)}
    for guess in guesses:
        for letter, state in zip(guess, _score_guess(guess, secret)):
            if PRIORITY[state] > PRIORITY[keyboard[letter]]:
                keyboard[letter] = state
    return keyboard


def _score_guess(guess: str, secret: str) -> list[str]:
    """
    Score each letter in the guess against the secret word.

    Two-pass approach to handle duplicate letters correctly:
    - Pass 1: mark correct positions, remove those letters from the pool
    - Pass 2: check remaining letters against the pool for present/absent
    """
    score = ["absent"] * 5
    pool = list(secret)

    # Pass 1 — correct (right letter, right position)
    for i, letter in enumerate(guess):
        if letter == secret[i]:
            score[i] = "correct"
            pool.remove(letter)

    # Pass 2 — present (right letter, wrong position)
    for i, letter in enumerate(guess):
        if score[i] == "correct":
            continue
        if letter in pool:
            score[i] = "present"
            pool.remove(letter)

    return score

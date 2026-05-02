"""Cleanup script — removes abandoned active games older than 30 minutes.

Run with: uv run python -m app.scripts.cleanup_games
Schedule with cron: */30 * * * * cd /path/to/backend && uv run python -m app.scripts.cleanup_games
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from sqlmodel import Session, select  # noqa: E402

from app.db import engine  # noqa: E402
from app.enums.game_status import GameStatus  # noqa: E402
from app.models.game import Game  # noqa: E402


def cleanup():
    # Games still active after 30 minutes are considered abandoned
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)

    with Session(engine) as session:
        abandoned = session.exec(
            select(Game).where(
                # Enable this when we start storing user win/loss
                # Game.status == GameStatus.ACTIVE,
                Game.created_at
                < cutoff,
            )
        ).all()

        for game in abandoned:
            session.delete(game)

        session.commit()
        print(f"Cleaned up {len(abandoned)} abandoned games")


if __name__ == "__main__":
    cleanup()

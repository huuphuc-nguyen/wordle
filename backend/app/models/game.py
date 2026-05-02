import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import ARRAY, String
from sqlmodel import Column, Field, SQLModel

from app.enums.game_status import GameStatus


class Game(SQLModel, table=True):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    secret_word: str = Field(max_length=5)
    guesses: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    attempts: int = Field(default=0)
    status: str = Field(default=GameStatus.ACTIVE)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

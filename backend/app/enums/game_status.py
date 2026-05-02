"""GameStatus — tracks the lifecycle of a game session."""

from enum import Enum


class GameStatus(str, Enum):
    ACTIVE = "active"   # game is in progress
    WON = "won"         # player guessed the word
    LOST = "lost"       # player used all 6 attempts

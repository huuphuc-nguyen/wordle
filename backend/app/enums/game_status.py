from enum import Enum


class GameStatus(str, Enum):
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"

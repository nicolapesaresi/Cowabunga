from enum import IntEnum


class States(IntEnum):
    """Render states for PygameRenderer."""

    MENU = 0
    GAME = 1
    GAMEOVER = 2
    PAUSE = 3
    LEADERBOARD = 4
    INFO = 5
    CLOSE = 6

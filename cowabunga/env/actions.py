from enum import IntEnum


class Action(IntEnum):
    """Action space for CowabungaEnv."""

    NOOP = 0
    LEFT = 1
    RIGHT = 2

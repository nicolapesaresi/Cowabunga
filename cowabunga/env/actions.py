from enum import IntEnum


class Action(IntEnum):
    """Action space for CowabungaEnv."""

    NOOP = 0  # no action
    LEFT = 1
    RIGHT = 2
    NOOP_DRAG = (
        3  # no action with drag commands: in this case that there's no animation to do.
    )

from enum import IntEnum


class Event(IntEnum):
    """Game events emitted by CowabungaEnv during a step.

    The env only reports what happened: renderers (sound, graphics) and RL agents
    decide what to do with it.
    """

    BOUNCE = 0  # a cow touched the paddle
    COW_SAVED = 1  # a cow safely crossed the river
    COW_LOST = 2  # a cow fell in the water
    GAME_OVER = 3  # last life lost

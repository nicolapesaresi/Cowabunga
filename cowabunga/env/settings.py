from cowabunga.py_game.commands import CommandModes

# env settings
WIDTH = 1600
HEIGHT = 900
# game settings
LIVES = 3
NEW_COW_PROB = 0.003
MAX_COWS_ON_SCREEN = 50

# objects settings
sea_level = HEIGHT * 0.95
# PADDLE
spot_0 = 0
spot_1 = WIDTH // 4 * 1
spot_2 = WIDTH // 2
spot_3 = WIDTH // 4 * 3
spot_4 = WIDTH

# CLIFF
left_cliff_height = HEIGHT / 3.4  # used both by Cow and Cliff
# other individual object settings are defined in their class

# pygame settings
FPS = 60
ACTION_COOLDOWN = 10  # number of frames you can't move after having moved
# this allows time for rendering the movement

# AESTHETICS
MAX_CLOUDS_ON_SCREEN = 7
NEW_CLOUD_PROB = 0.005

DEFAULT_USERNAME = "Cowboy"

DEFAULT_COMMANDS = CommandModes.DRAG

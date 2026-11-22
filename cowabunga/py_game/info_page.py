import pygame
from pygame.sprite import Group

from cowabunga.env import settings
from cowabunga.env.actions import Action
from cowabunga.env.settings import ACTION_COOLDOWN
from cowabunga.py_game.commands import CommandModes
from cowabunga.py_game.sprites.button import BackButton, CogsButton
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.sprites.text import PageTitle, TextSprite
from cowabunga.py_game.states import States
from cowabunga.py_game.volume_controls import draw_panel

PANEL_TOP = settings.HEIGHT * 0.27
PANEL_BOTTOM = settings.HEIGHT * 0.8
PANEL_WIDTH = settings.WIDTH * 0.6


class InfoPage:
    """Page displaying instructions and credits."""

    def __init__(self, commands: CommandModes, paddle: PaddleSprite):
        """Instantiates InfoPage class.

        Args:
            commands: command mode for the paddle.
            paddle: paddle sprite to be rendered on info page.
        """
        self.paddle = paddle
        self.commands = commands
        self.back_button = BackButton()
        # cogs on the right of the controls lines, inside the panel
        self.cogs_button = CogsButton((settings.WIDTH * 0.74, settings.HEIGHT * 0.505))
        self.buttons = Group(self.back_button, self.cogs_button)

        self.command_lines = {
            CommandModes.CLICK: "Right/left arrow or click on the screen - move paddle",
            CommandModes.DRAG: "Move mouse or drag - move paddle",
        }
        self.update_lines()

        self.frames_since_last_move = 0  # for paddle movement in page

    def update_lines(self):
        """Rebuilds info page texts based on current commands."""
        fonts = {
            "header": pygame.font.Font(None, settings.HEIGHT // 22),
            "text": pygame.font.Font(None, settings.HEIGHT // 28),
        }
        color = {"header": "yellow", "text": "white"}
        # (text, style, vertical center as fraction of the screen height)
        lines = [
            ("Controls", "header", 0.43),
            (self.command_lines[self.commands], "text", 0.485),
            ("Spacebar, Esc or pause button - pause game", "text", 0.525),
            ("Credits", "header", 0.62),
            ("Original game and idea by Mark Andrade - AndradeArts", "text", 0.675),
            ("Pygame version created by Nicola Pesaresi", "text", 0.715),
            ("Music and sounds by Lorenzo Previati", "text", 0.755),
        ]
        self.sprites = Group(PageTitle("Info"))
        for text, style, y in lines:
            sprite = TextSprite(text, fonts[style], color[style], (0, 0))
            sprite.rect.center = (settings.WIDTH // 2, int(settings.HEIGHT * y))
            self.sprites.add(sprite)

    def update(self):
        """Updates according to paddle input."""
        # move paddle in menù
        action = self.paddle.get_key_input(self.commands)
        if action in (Action.LEFT, Action.RIGHT) and self.frames_since_last_move >= ACTION_COOLDOWN:
            self.paddle.paddle.move(action)
            self.frames_since_last_move = 0
        else:  # noqa: PLR5501
            if action != Action.NOOP_DRAG:
                self.paddle.paddle.animate_move()
        self.frames_since_last_move += 1

    def draw(self, screen: pygame.Surface):
        """Draws the page. Must be called after PygameRenderer.draw_screen() to have background.

        Args:
            screen: pygame surface to draw on.
        """
        draw_panel(screen, PANEL_TOP, PANEL_BOTTOM, PANEL_WIDTH)
        self.sprites.draw(screen)
        self.buttons.draw(screen)

    def toggle_commands(self):
        """Switches between click and drag commands."""
        self.commands = CommandModes.DRAG if self.commands == CommandModes.CLICK else CommandModes.CLICK
        self.update_lines()

    def handle_events(self) -> tuple[States, CommandModes]:
        """Handles info page events.

        Returns:
            render_state: outcome of event handling.
            commands: the (possibly changed) command mode.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE, self.commands
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return States.MENU, self.commands
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.clicked(event.pos):
                    return States.MENU, self.commands
                if self.cogs_button.clicked(event.pos):
                    self.toggle_commands()
        return States.INFO, self.commands

import pygame
from pygame.sprite import Group
import cowabunga.env.settings as settings
from cowabunga.py_game.states import States
from cowabunga.py_game.sprites.text import TextSprite
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.sprites.button import BackButton, CogsButton
from cowabunga.env.actions import Action
from cowabunga.env.settings import ACTION_COOLDOWN
from cowabunga.py_game.commands import CommandModes


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
        self.buttons = Group()
        self.buttons.add(BackButton(), CogsButton())

        self.command_lines = {
            CommandModes.CLICK: "Right/left arrow or click on the screen - move paddle",
            CommandModes.DRAG: "Move mouse or drag - move paddle",
        }

        self.frames_since_last_move = 0  # for paddle movement in page

    def update_lines(self):
        """Updates info page texts based on commands."""
        self.sprites = pygame.sprite.Group()
        color = {"header": "yellow", "text": "white"}
        font_size = {"header": settings.HEIGHT // 15, "text": settings.HEIGHT // 25}
        start_y = int(settings.HEIGHT * 0.3)
        spacing = font_size["text"] * 1.75

        # update lines based on commands - tuples (text, style)
        self.lines = [
            ("Commands", "header"),
            (self.command_lines[self.commands], "text"),
            ("Spacebar - pause game", "text"),
            ("Credits", "header"),
            ("Original game and idea by Mark Andrade - AndradeArts", "text"),
            ("Pygame version created by Nicola Pesaresi", "text"),
        ]

        for i, (text, style) in enumerate(self.lines):
            y = start_y + i * spacing
            sprite = TextSprite(
                text=text,
                font=pygame.font.Font(None, font_size[style]),
                color=color[style],
                pos=(settings.WIDTH // 2, y),
            )
            sprite.rect.centerx = settings.WIDTH // 2
            self.sprites.add(sprite)

    def update(self):
        """Updates according to paddle input."""
        self.update_lines()
        # move paddle in menù
        action = self.paddle.get_key_input(self.commands)
        if (
            action in (Action.LEFT, Action.RIGHT)
            and self.frames_since_last_move >= ACTION_COOLDOWN
        ):
            self.paddle.paddle.move(action)
            self.frames_since_last_move = 0
        else:
            if action != Action.NOOP_DRAG:
                self.paddle.paddle.animate_move()
        self.frames_since_last_move += 1

    def draw(self, screen: pygame.Surface):
        """Draw all lines centered and buttons.
        Args:
            screen: pygame surface to draw on.
        """
        self.sprites.draw(screen)
        self.buttons.draw(screen)

    def handle_events(self) -> States:
        """Handles info page events.
        Returns:
            render_state: outcome of event handling.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE, self.commands
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons.sprites():
                    if isinstance(button, BackButton) and button.clicked(event.pos):
                        return States.MENU, self.commands
                    elif isinstance(button, CogsButton) and button.clicked(event.pos):
                        if self.commands == CommandModes.CLICK:
                            self.commands = CommandModes.DRAG
                        elif self.commands == CommandModes.DRAG:
                            self.commands = CommandModes.CLICK
        return States.INFO, self.commands

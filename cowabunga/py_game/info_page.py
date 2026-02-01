import pygame
from pygame.sprite import Group
import cowabunga.env.settings as settings
from cowabunga.py_game.states import States
from cowabunga.py_game.sprites.text import TextSprite
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.sprites.button import BackButton
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
        self.buttons.add(BackButton())

        # lines are tuples (text, style)
        self.lines = [
            ("Commands", "header"),
            ("Right/left arrow or click on the screen - move paddle that way", "text"),
            ("Spacebar - pause game", "text"),
            ("Credits", "header"),
            ("Original game and idea by Mark Andrade - AndradeArts", "text"),
            ("Pygame version created by Nicola Pesaresi", "text"),
        ]

        self.sprites = pygame.sprite.Group()
        color = {"header": "yellow", "text": "white"}
        font_size = {"header": settings.HEIGHT // 15, "text": settings.HEIGHT // 25}
        start_y = int(settings.HEIGHT * 0.3)
        spacing = font_size["text"] * 1.75

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

        self.frames_since_last_move = 0  # for paddle movement in page

    def update(self):
        """Updates according to paddle input."""
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
                return States.CLOSE
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons.sprites():
                    if isinstance(button, BackButton) and button.clicked(event.pos):
                        return States.MENU
        return States.INFO

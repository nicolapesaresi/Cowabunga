import pygame
from pygame.sprite import Group
import cowabunga.env.settings as settings
from cowabunga.pygame.states import States
from cowabunga.pygame.sprites.text import TextSprite
from cowabunga.pygame.sprites.paddle import PaddleSprite
from cowabunga.pygame.sprites.button import BackButton


class InfoPage:
    """Page displaying instructions and credits."""

    def __init__(self, paddle: PaddleSprite):
        """Instantiates InfoPage class.
        Args:
            paddle: paddle sprite to be rendered on info page.
        """
        self.paddle = paddle
        self.buttons = Group()
        self.buttons.add(BackButton())

        # lines are tuples (text, style)
        self.lines = [
            ("Commands", "header"),
            ("Left arrow / Right arrow - move paddle", "text"),
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

    def update(self):
        """Updates according to paddle input."""
        self.paddle.get_key_input()

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

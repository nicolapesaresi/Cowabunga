import pygame
from pygame.sprite import Group
from cowabunga.py_game.sprites.text import PauseText
from cowabunga.py_game.sprites.button import PauseButton
from cowabunga.py_game.states import States


class PauseScreen:
    """Handles pause screen for Cowabunga."""

    def __init__(self):
        """Instantiates screen elements."""
        self.buttons = Group()
        self.buttons.add(PauseButton())
        self.pause_texts = Group()
        self.pause_texts.add(PauseText())

    def draw(self, screen: pygame.Surface):
        """Draw the pause screen. Must be called after PygameRenderer.draw_screen() to have background.
        Args:
            screen: surface to draw on.
        """
        self.buttons.draw(screen)
        self.pause_texts.draw(screen)

    def handle_events(self) -> States:
        """Handles pause events.
        Returns:
            render_state: outcome of event handling.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return States.GAME
        return States.PAUSE

import pygame
from pygame.sprite import Group

from cowabunga.env import settings
from cowabunga.py_game.audio import AudioManager
from cowabunga.py_game.sprites.button import BackButton
from cowabunga.py_game.sprites.text import TextSprite
from cowabunga.py_game.states import States
from cowabunga.py_game.volume_controls import VolumeControls, draw_panel


class SettingsPage:
    """Sound settings page, opened from the main menu."""

    def __init__(self, audio: AudioManager):
        """Instantiates the page.

        Args:
            audio: the game's audio manager.
        """
        self.buttons = Group(BackButton())
        title = TextSprite(
            text="Sound",
            font=pygame.font.Font(None, settings.HEIGHT // 12),
            color="yellow",
            pos=(settings.WIDTH // 2, settings.HEIGHT * 0.3),
        )
        title.rect.centerx = settings.WIDTH // 2
        self.texts = Group(title)
        self.controls = VolumeControls(audio, settings.HEIGHT * 0.46)

    def draw(self, screen: pygame.Surface):
        """Draws the page. Must be called after PygameRenderer.draw_screen() to have background.

        Args:
            screen: surface to draw on.
        """
        draw_panel(screen, settings.HEIGHT * 0.27, settings.HEIGHT * 0.67)
        self.texts.draw(screen)
        self.controls.draw(screen)
        self.buttons.draw(screen)

    def handle_events(self) -> States:
        """Handles settings page events.

        Returns:
            render_state: outcome of event handling.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE
            if self.controls.handle_event(event):
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return States.MENU
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons.sprites():
                    if button.clicked(event.pos):
                        return States.MENU
        return States.SETTINGS

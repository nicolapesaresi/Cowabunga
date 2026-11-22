import pygame
from pygame.sprite import Group

from cowabunga.env import settings
from cowabunga.py_game.audio import AudioManager
from cowabunga.py_game.sprites.button import TextButton
from cowabunga.py_game.sprites.text import TextSprite
from cowabunga.py_game.states import States
from cowabunga.py_game.volume_controls import VolumeControls, draw_panel


class PauseScreen:
    """Pause screen: volume settings, resume and back to the main menu."""

    def __init__(self, audio: AudioManager):
        """Instantiates screen elements.

        Args:
            audio: the game's audio manager.
        """
        self.texts = Group()
        for text, size, color, y in (
            ("Paused", settings.HEIGHT // 10, "yellow", settings.HEIGHT * 0.2),
            ("Space or Esc to continue", settings.HEIGHT // 28, "white", settings.HEIGHT * 0.74),
        ):
            sprite = TextSprite(text, pygame.font.Font(None, size), color, (0, y))
            sprite.rect.centerx = settings.WIDTH // 2
            self.texts.add(sprite)
        self.controls = VolumeControls(audio, settings.HEIGHT * 0.37)
        self.resume_button = TextButton("Resume", (settings.WIDTH * 0.42, settings.HEIGHT * 0.63))
        self.menu_button = TextButton("Main menu", (settings.WIDTH * 0.58, settings.HEIGHT * 0.63))
        self.buttons = Group(self.resume_button, self.menu_button)

    def draw(self, screen: pygame.Surface):
        """Draw the pause screen. Must be called after PygameRenderer.draw_screen() to have background.

        Args:
            screen: surface to draw on.
        """
        draw_panel(screen, settings.HEIGHT * 0.16, settings.HEIGHT * 0.8)
        self.texts.draw(screen)
        self.controls.draw(screen)
        self.buttons.draw(screen)

    def handle_events(self) -> States:
        """Handles pause events.

        Returns:
            render_state: GAME to resume, MENU to quit the game, PAUSE to stay, CLOSE to exit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE
            if self.controls.handle_event(event):
                continue
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                return States.GAME
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.resume_button.clicked(event.pos):
                    return States.GAME
                if self.menu_button.clicked(event.pos):
                    return States.MENU
        return States.PAUSE

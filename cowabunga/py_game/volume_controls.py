import pygame
from pygame.sprite import Group

from cowabunga.env import settings
from cowabunga.py_game.audio import AudioManager
from cowabunga.py_game.sprites.slider import VolumeSlider


class VolumeControls:
    """Music and sound effects sliders, shared by the settings page and the pause screen."""

    def __init__(self, audio: AudioManager, top_y: float):
        """Instantiates the sliders with the current audio levels.

        Args:
            audio: the game's audio manager, updated live while sliding.
            top_y: vertical center of the first slider.
        """
        self.audio = audio
        self.music = VolumeSlider("Music", audio.music_level, top_y)
        self.sfx = VolumeSlider("Sound effects", audio.sfx_level, top_y + settings.HEIGHT * 0.13)
        self.sliders = Group(self.music, self.sfx)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Updates the audio levels from slider events.

        Returns:
            (bool): whether the event was used by a slider.
        """
        result = self.music.handle_event(event)
        if result:
            self.audio.set_music_level(self.music.value)
            return True
        result = self.sfx.handle_event(event)
        if result:
            self.audio.set_sfx_level(self.sfx.value)
            if result == "release":
                self.audio.preview_sfx()  # let the player hear the new effects volume
            return True
        return False

    def draw(self, screen: pygame.Surface):
        """Draws the sliders.

        Args:
            screen: surface to draw on.
        """
        self.sliders.draw(screen)


def draw_panel(screen: pygame.Surface, top: float, bottom: float, width: float = settings.WIDTH * 0.42):
    """Draws a translucent rounded panel behind menus, to keep text readable on the background.

    Args:
        screen: surface to draw on.
        top: y of the panel top.
        bottom: y of the panel bottom.
        width: panel width (centered horizontally).
    """
    panel = pygame.Surface((int(width), int(bottom - top)), pygame.SRCALPHA)
    pygame.draw.rect(panel, (20, 30, 50, 240), panel.get_rect(), border_radius=int(settings.HEIGHT * 0.04))
    screen.blit(panel, ((settings.WIDTH - width) / 2, top))

import pygame
from pygame._sdl2.video import Renderer, Texture

from cowabunga.env import settings


class GameWindow:
    """Resizable desktop window showing a fixed-resolution canvas, scaled to fit and letterboxed.

    The game draws on `canvas` at the logical resolution (settings.WIDTH x settings.HEIGHT), so game
    coordinates never depend on the window size. Mouse event positions are mapped to logical
    coordinates by SDL; use `mouse_pos()` instead of `pygame.mouse.get_pos()`.
    """

    active: "GameWindow | None" = None  # the open window, if any (None in the browser)

    def __init__(self, title: str):
        logical_size = (settings.WIDTH, settings.HEIGHT)
        self.window = pygame.Window(title, size=self._initial_size(), resizable=True)
        self.window.minimum_size = (settings.WIDTH // 4, settings.HEIGHT // 4)
        self.renderer = Renderer(self.window)
        self.renderer.logical_size = logical_size  # SDL scales to the window and maps mouse events
        self.renderer.draw_color = (0, 0, 0, 255)  # letterbox bars
        self.canvas = pygame.Surface(logical_size)
        self.texture = Texture(self.renderer, logical_size, streaming=True)
        GameWindow.active = self

    @staticmethod
    def _initial_size() -> tuple[int, int]:
        """Default window size, capped to fit the desktop while keeping the aspect ratio."""
        width, height = settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT
        desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
        scale = min(1.0, 0.85 * desktop_w / width, 0.85 * desktop_h / height)
        return int(width * scale), int(height * scale)

    def present(self):
        """Shows the current canvas in the window."""
        self.texture.update(self.canvas)
        self.renderer.clear()
        self.renderer.blit(self.texture)
        self.renderer.present()

    def to_logical(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Converts window pixel coordinates to logical game coordinates."""
        x, y = self.renderer.coordinates_from_window(pos)
        return int(x), int(y)


def mouse_pos() -> tuple[int, int]:
    """Mouse position in logical game coordinates (desktop window or browser canvas).

    Returns (0, 0) as long as the mouse has never been over the window, like pygame.mouse.get_pos().
    """
    pos = pygame.mouse.get_pos()
    if GameWindow.active is None or pos == (0, 0):
        return pos
    return GameWindow.active.to_logical(pos)

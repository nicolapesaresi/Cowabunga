import pygame

from cowabunga.env import settings


class VolumeSlider(pygame.sprite.Sprite):
    """Horizontal slider with a label and a percentage, for values from 0 to 1.

    Drag the knob or click anywhere on the bar. Works with mouse and touch
    (pygame turns touches into mouse events).
    """

    def __init__(self, label: str, value: float, center_y: float, width: float = settings.WIDTH * 0.3):
        """Instantiates the slider.

        Args:
            label: text shown above the bar.
            value: initial value, from 0 to 1.
            center_y: vertical position of the slider center.
            width: width of the bar.
        """
        super().__init__()
        self.label = label
        self.value = value
        self.dragging = False
        self.bar_width = int(width)
        self.knob_radius = int(settings.HEIGHT * 0.022)
        self.bar_height = max(6, int(settings.HEIGHT * 0.012))
        self.font = pygame.font.Font(None, settings.HEIGHT // 22)
        height = int(settings.HEIGHT * 0.1)
        self.rect = pygame.Rect(0, 0, self.bar_width + 2 * self.knob_radius, height)
        self.rect.center = (settings.WIDTH // 2, int(center_y))
        self.bar_y = int(height * 0.72)  # bar position inside the sprite
        self.render()

    def render(self):
        """Redraws the slider image for the current value."""
        image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        label = self.font.render(self.label, True, "white")
        percent = self.font.render(f"{round(self.value * 100)}%", True, "yellow")
        image.blit(label, (self.knob_radius, 0))
        image.blit(percent, (self.rect.width - self.knob_radius - percent.get_width(), 0))

        bar = pygame.Rect(self.knob_radius, self.bar_y - self.bar_height // 2, self.bar_width, self.bar_height)
        pygame.draw.rect(image, (255, 255, 255, 90), bar, border_radius=self.bar_height // 2)
        filled = bar.copy()
        filled.width = max(1, int(self.bar_width * self.value))
        pygame.draw.rect(image, (255, 215, 0), filled, border_radius=self.bar_height // 2)
        knob = (self.knob_radius + int(self.bar_width * self.value), self.bar_y)
        pygame.draw.circle(image, "white", knob, self.knob_radius)
        pygame.draw.circle(image, (255, 215, 0), knob, self.knob_radius, width=3)
        self.image = image

    def _on_bar(self, pos: tuple[int, int]) -> bool:
        x, y = pos[0] - self.rect.x, pos[1] - self.rect.y
        return 0 <= x <= self.rect.width and abs(y - self.bar_y) <= self.knob_radius * 1.6

    def _set_from_x(self, x: int):
        self.value = min(1.0, max(0.0, (x - self.rect.x - self.knob_radius) / self.bar_width))
        self.render()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handles mouse events.

        Returns:
            "drag" while the value changes, "release" when the player lets go, otherwise None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._on_bar(event.pos):
            self.dragging = True
            self._set_from_x(event.pos[0])
            return "drag"
        if event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_from_x(event.pos[0])
            return "drag"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            return "release"
        return None

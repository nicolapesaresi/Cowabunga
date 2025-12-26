import pygame
import time
import cowabunga.env.settings as settings


class TextBoxSprite(pygame.sprite.Sprite):
    """Text input box sprite."""

    def __init__(
        self,
        x: int = settings.WIDTH // 2 - settings.WIDTH / 18,
        y: int = settings.HEIGHT * 0.02,
        w: int = settings.WIDTH / 9,
        h: int = settings.HEIGHT * 0.04,
        font: pygame.font.Font | None = None,
        text: str = "Enter name",
        max_length: int = 12,
        text_color: str | tuple[int, int, int] = "white",
        box_color: str | tuple[int, int, int] = "white",
        active_color: str | tuple[int, int, int] = "yellow",
        bg_color: str | tuple[int, int, int] = "black",
        border_radius: int = 8,
    ):
        """Instantiates text input box.
        Args:
            x: x coord of top left corner.
            y: y coord of top left corner.
            w: width of the textbox.
            h: height of the textbox.
            font: font of the text.
            text: initial text in the textbox.
            max_length: maximum length of text input.
            text_color: color of the text.
            box_color: color of the box border when inactive.
            active_color: color of the box border when active.
            bg_color: background color of the textbox.
            border_radius: border radius of the textbox.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        if font is None:
            font = pygame.font.Font(None, int(settings.HEIGHT * 0.03))
        self.font = font
        self.max_length = max_length

        self.text = text
        self.active = False

        self.text_color = text_color
        self.box_color = box_color
        self.active_color = active_color
        self.bg_color = bg_color
        self.border_radius = border_radius

        self.last_blink = time.time()
        self.cursor_visible = True

        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.update_image()

    def handle_event(self, event):
        """Handles pygame events for text input.
        Args:
            event: pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode

    def update_image(self):
        """Updates the textbox image."""
        self.image.fill((0, 0, 0, 0))
        border_color = self.active_color if self.active else self.box_color
        pygame.draw.rect(
            self.image,
            border_color,
            self.image.get_rect(),
            width=2,
            border_radius=self.border_radius,
        )
        txt = self.text
        color = self.text_color
        txt_surf = self.font.render(txt, True, color)

        # center text horizontally and vertically
        x = (self.rect.width - txt_surf.get_width()) // 2
        y = (self.rect.height - txt_surf.get_height()) // 2
        self.image.blit(txt_surf, (x, y))

        # cursor blink
        if self.active:
            now = time.time()
            if now - self.last_blink > 0.5:
                self.cursor_visible = not self.cursor_visible
                self.last_blink = now

            if self.cursor_visible:
                cursor_x = x + txt_surf.get_width()  # cursor right after text
                pygame.draw.line(
                    self.image,
                    self.text_color,
                    (cursor_x, 8),
                    (cursor_x, self.rect.height - 8),
                    2,
                )

    def update(self):
        """Updates the textbox sprite."""
        self.update_image()

import pygame
import cowabunga.env.settings as settings
from cowabunga.py_game.sprites.text import TextSprite
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.states import States
from cowabunga.py_game.sprites.button import BackButton
from pygame.sprite import Group


class LeaderboardRow(TextSprite):
    """Single row of Leaderboards table."""

    def __init__(self, rank: int, name: str, score: int, timestamp, y: int):
        """Instantiates leaderboard row.
        Args:
            rank: ranking in the leaderboards.
            name: name of the player.
            score: points scored.
            timestamp: timestamp of record.
            y: y coord of the row.
        """
        text = f"{rank:>2}.   " f"{name:<12}   " f"{score:<6}   " f"{timestamp:>5}"
        font = pygame.font.Font(None, settings.HEIGHT // 22)
        color = "white"
        pos = (settings.WIDTH // 2, y)
        super().__init__(text, font, color, pos)
        self.base_y = y
        self.rect.centerx = settings.WIDTH // 2


class LeaderboardScreen:
    """Handles leaderboard screen for Cowabunga."""

    def __init__(self, paddle: PaddleSprite, scores: list[dict]):
        """Instantiates main menù elements.
        Args:
            paddle: paddle sprite from pygame renderer.
        """
        self.paddle = paddle
        self.scores = sorted(
            scores,
            key=lambda s: s["score"],
            reverse=True,
        )

        self.rows = Group()
        self.buttons = Group()
        self.buttons.add(BackButton())

        self.row_height = settings.HEIGHT // 22
        self.start_y = int(settings.HEIGHT * 0.3)
        self.visible_rows = 10

        self.scroll_y = 0
        self.top_y = self.start_y
        self.bottom_y = self.start_y + self.visible_rows * self.row_height

        # create row sprites
        for i, row in enumerate(self.scores):
            sprite = LeaderboardRow(
                rank=i + 1,
                name=row["name"],
                score=row["score"],
                timestamp=row["timestamp"],
                y=self.start_y + i * self.row_height,
            )
            self.rows.add(sprite)

        self.max_scroll = max(
            0,
            len(self.rows) * self.row_height - self.visible_rows * self.row_height,
        )

    def update(self):
        """Updates leaderboard page."""
        self.paddle.get_key_input()
        # scrolling
        self.scroll_y = max(-self.max_scroll, min(0, self.scroll_y))
        for row in self.rows:
            row.rect.y = row.base_y + self.scroll_y

    def draw(self, screen: pygame.Surface):
        """Draw the leaderboard page. Must be called after PygameRenderer.draw_screen() to have background.
        Args:
            screen: surface to draw on.
        """
        for row in self.rows:
            if self.top_y <= row.rect.y < self.bottom_y:
                screen.blit(row.image, row.rect)
        self.buttons.draw(screen)

    def handle_events(self) -> States:
        """Handles leaderboard events.
        Returns:
            render_state: outcome of event handling.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE

            if event.type == pygame.MOUSEWHEEL:
                self.scroll_y += event.y * self.row_height

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.scroll_y += self.row_height
                elif event.key == pygame.K_DOWN:
                    self.scroll_y -= self.row_height

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if isinstance(button, BackButton) and button.clicked(event.pos):
                        return States.MENU

        return States.LEADERBOARD

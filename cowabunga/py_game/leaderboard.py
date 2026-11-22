import pygame
from pygame.sprite import Group

from cowabunga.env import settings
from cowabunga.env.actions import Action
from cowabunga.py_game.commands import CommandModes
from cowabunga.py_game.sprites.button import BackButton
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.sprites.text import PageTitle, TextSprite
from cowabunga.py_game.states import States
from cowabunga.py_game.volume_controls import draw_panel

PANEL_TOP = settings.HEIGHT * 0.27
PANEL_BOTTOM = settings.HEIGHT * 0.83
PANEL_WIDTH = settings.WIDTH * 0.6

# column anchors as offsets from the screen center: (offset, alignment)
COLUMNS = (
    (-0.25 * settings.WIDTH, "right"),  # rank
    (-0.23 * settings.WIDTH, "left"),  # name
    (0.04 * settings.WIDTH, "right"),  # score
    (0.25 * settings.WIDTH, "right"),  # date
)


class LeaderboardRow(pygame.sprite.Sprite):
    """Single row of Leaderboards table, with aligned columns."""

    def __init__(self, cells: tuple[str, str, str, str], y: int, color: str = "white"):
        """Instantiates leaderboard row.

        Args:
            cells: rank, name, score and timestamp texts.
            y: y coord of the row top.
            color: text color.
        """
        super().__init__()
        font = pygame.font.Font(None, settings.HEIGHT // 22)
        self.image = pygame.Surface((int(PANEL_WIDTH), font.get_height()), pygame.SRCALPHA)
        center = PANEL_WIDTH / 2
        for text, (offset, align) in zip(cells, COLUMNS, strict=True):
            cell = font.render(text, True, color)
            x = center + offset - (cell.get_width() if align == "right" else 0)
            self.image.blit(cell, (x, 0))
        self.rect = self.image.get_rect(midtop=(settings.WIDTH // 2, y))
        self.base_y = y


class LeaderboardScreen:
    """Handles leaderboard screen for Cowabunga."""

    def __init__(self, commands: CommandModes, paddle: PaddleSprite, scores: list[dict]):
        """Instantiates main menù elements.

        Args:
            commands: command mode for moving paddle
            paddle: paddle sprite from pygame renderer.
            scores: list of highscores to display.
        """
        self.commands = commands
        self.paddle = paddle
        self.scores = sorted(
            scores,
            key=lambda s: s["score"],
            reverse=True,
        )

        self.rows = Group()
        self.buttons = Group()
        self.buttons.add(BackButton())

        self.texts = Group(PageTitle("Records"))
        self.header = LeaderboardRow(("#", "Name", "Score", "Date"), int(settings.HEIGHT * 0.395), "yellow")
        self.texts.add(self.header)
        if not self.scores:
            empty = TextSprite(
                "No records yet - go play!", pygame.font.Font(None, settings.HEIGHT // 28), "white", (0, 0)
            )
            empty.rect.center = (settings.WIDTH // 2, int(settings.HEIGHT * 0.58))
            self.texts.add(empty)

        self.row_height = settings.HEIGHT // 22
        self.start_y = int(settings.HEIGHT * 0.45)
        self.visible_rows = 8

        self.scroll_y = 0
        self.top_y = self.start_y
        self.bottom_y = self.start_y + self.visible_rows * self.row_height

        # create row sprites
        for i, row in enumerate(self.scores):
            sprite = LeaderboardRow(
                cells=(f"{i + 1}.", str(row["name"]), str(row["score"]), str(row["timestamp"])),
                y=self.start_y + i * self.row_height,
            )
            self.rows.add(sprite)

        self.max_scroll = max(
            0,
            len(self.rows) * self.row_height - self.visible_rows * self.row_height,
        )

        self.frames_since_last_move = 0  # for paddle movement

    def update(self):
        """Updates leaderboard page."""
        # move paddle in page
        action = self.paddle.get_key_input(self.commands)
        if action in (Action.LEFT, Action.RIGHT) and self.frames_since_last_move >= settings.ACTION_COOLDOWN:
            self.paddle.paddle.move(action)
            self.frames_since_last_move = 0
        else:  # noqa: PLR5501
            if action != Action.NOOP_DRAG:
                self.paddle.paddle.animate_move()
        self.frames_since_last_move += 1

        # scrolling
        self.scroll_y = max(-self.max_scroll, min(0, self.scroll_y))
        for row in self.rows:
            row.rect.y = row.base_y + self.scroll_y

    def draw(self, screen: pygame.Surface):
        """Draw the leaderboard page.
        Must be called after PygameRenderer.draw_screen() to have background.

        Args:
            screen: surface to draw on.
        """
        draw_panel(screen, PANEL_TOP, PANEL_BOTTOM, PANEL_WIDTH)
        self.texts.draw(screen)
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
                if event.key == pygame.K_ESCAPE:
                    return States.MENU
                if event.key == pygame.K_UP:
                    self.scroll_y += self.row_height
                elif event.key == pygame.K_DOWN:
                    self.scroll_y -= self.row_height

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if isinstance(button, BackButton) and button.clicked(event.pos):
                        return States.MENU

        return States.LEADERBOARD

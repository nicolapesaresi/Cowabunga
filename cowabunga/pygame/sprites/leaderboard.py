import pygame
import cowabunga.env.settings as settings

# import pandas as pd
from cowabunga.pygame.sprites.text import TextSprite
# from datetime import datetime


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


# class LeaderboardScreen:
#     """Leaderboard table object."""

#     def __init__(self, df: pd.DataFrame):
#         """Instantiates leaderboard table.
#         Args:
#             df: highscores dataframe.
#         """
#         self.df = df

#         self.rows = pygame.sprite.Group()
#         self.row_height = settings.HEIGHT // 22
#         self.start_y = int(settings.HEIGHT * 0.3)
#         self.scroll_y = 0
#         self.visible_rows = 10
#         self.top_y = self.start_y
#         self.bottom_y = self.start_y + self.visible_rows * self.row_height

#         for i, row in df.iterrows():
#             sprite = LeaderboardRow(
#                 rank=i + 1,
#                 name=row["name"],
#                 score=row["score"],
#                 timestamp=row["timestamp"],
#                 y=self.start_y + i * self.row_height,
#             )
#             self.rows.add(sprite)

#         self.max_scroll = max(
#             0,
#             len(self.rows) * self.row_height - self.visible_rows * self.row_height,
#         )

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEWHEEL:
#             self.scroll_y += event.y * self.row_height

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 self.scroll_y += self.row_height
#             elif event.key == pygame.K_DOWN:
#                 self.scroll_y -= self.row_height

#         self.scroll_y = max(-self.max_scroll, min(0, self.scroll_y))

#     def draw(self, screen):
#         for row in self.rows:
#             row.rect.y = row.base_y + self.scroll_y

#             if self.top_y <= row.rect.y < self.bottom_y:
#                 screen.blit(row.image, row.rect)

import pygame
from pygame.sprite import Group
from cowabunga.pygame.sprites.text import (
    GameOverText,
    FinalScoreSprite,
    PressToGoToMenuText,
)
from cowabunga.pygame.states import States


class GameOver:
    """Handles game over screen for Cowabunga."""

    def __init__(self, score: int):
        """Instantiates game over screen elements.
        Args:
            score: final score of the game.
        """
        self.score = score
        self.game_over_texts = Group()
        self.game_over_texts.add(
            GameOverText(), FinalScoreSprite(self.score), PressToGoToMenuText()
        )

    def draw(self, screen: pygame.Surface):
        """Draw the game over screen. Must be called after PygameRenderer.draw_screen() to have background.
        Args:
            screen: surface to draw on.
        """
        self.game_over_texts.draw(screen)

    def handle_events(self) -> States:
        """Handles main menù events.
        Returns:
            render_state: outcome of event handling.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return States.MENU
        return States.GAMEOVER

import asyncio  # noqa: I001
import numpy  # needed here, otherwise pygbag breaks  # noqa: F401

import pygame

from cowabunga.env import settings
from cowabunga.py_game.game import PygameRenderer
from cowabunga.py_game.states import States

pygame.mixer.pre_init(44100, -16, 2, 512)  # small buffer: low latency for bounce notes
pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))


async def main():
    """Async pygbag loop. Game logic lives in PygameRenderer.update_state, shared with desktop."""
    game = PygameRenderer(screen)
    game.clock = pygame.time.Clock()
    game.load_gamescreen()
    game.draw_screen()
    render_state = game.initial_state

    while render_state != States.CLOSE:
        render_state = game.update_state(render_state)
        pygame.display.flip()
        game.clock.tick(settings.FPS)
        await asyncio.sleep(0)


asyncio.run(main())

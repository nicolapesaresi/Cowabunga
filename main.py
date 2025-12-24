import asyncio
import pygame
import numpy  # needed here, otherwise pygbag breaks  # noqa: F401
from cowabunga.pygame.game import PygameRenderer

pygame.init()
screen = pygame.display.set_mode((400, 200))

game = PygameRenderer(screen)
coords = (0, 0, 100, 50)


async def main():
    count = 1000000
    global coords
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        coords = (coords[0] + 1, coords[1] + 1, coords[1] + 1, coords[1] + 1)
        game.screen.fill((0, 0, 0))
        pygame.draw.rect(game.screen, (255, 255, 255), coords)
        pygame.display.flip()

        await asyncio.sleep(0)

        count -= 1
        if count < 0:
            return


asyncio.run(main())

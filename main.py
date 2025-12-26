import asyncio
import numpy  # needed here, otherwise pygbag breaks  # noqa: F401

import pygame
import cowabunga.env.settings as settings
from datetime import datetime
from cowabunga.py_game.states import States
from cowabunga.py_game.game import PygameRenderer

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))


async def main():
    game = PygameRenderer(screen)
    game.clock = pygame.time.Clock()
    game.load_gamescreen()
    game.draw_screen()
    render_state = game.initial_state

    while True:
        if render_state == States.CLOSE:
            return

        elif render_state == States.MENU:
            render_state = game.main_menu()

        elif render_state == States.INFO:
            render_state = game.info_page()

        elif render_state == States.LEADERBOARD:
            render_state = game.leadernoard_page()

        elif render_state == States.GAMEOVER:
            render_state = game.gameover_screen()

        elif render_state == States.PAUSE:
            render_state = game.pause_game()

        elif render_state == States.GAME:
            # main game logic

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    render_state = States.CLOSE
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    render_state = States.PAUSE

            # player input and env update
            game.paddle.get_key_input()
            game.env.step(0)
            game.update_cows()

            # draw new screen
            game.draw_screen()
            game.draw_text()

            # check game finished
            if game.env.done:
                game.update_highscores(
                    name=game.username,
                    points=game.env.score,
                    timestamp=datetime.now(),
                )
                render_state = States.GAMEOVER
        pygame.display.flip()
        game.clock.tick(settings.FPS)
        if game.env.done:
            render_state = States.GAMEOVER
        await asyncio.sleep(0)


asyncio.run(main())

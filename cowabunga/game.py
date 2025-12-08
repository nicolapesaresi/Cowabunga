import pygame
import random
from pygame.sprite import Group

from utils.constants import WIDTH, HEIGHT, FPS, WHITE, BLUE, BROWN, LIGHT_BLUE, GREEN
from utils.cow import Cow
from utils.cliff import LeftCliff, RightCliff
from utils.paddle import Paddle
from utils.utils import create_sprite

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cowabunga - Pygame Edition")


# Game variables
paddle = create_sprite(Paddle)
leftcliff = create_sprite(LeftCliff)
rightcliff = create_sprite(RightCliff)

cliffs = Group()
cliffs.add(leftcliff, rightcliff)
player = Group()
player.add(paddle)

cow = create_sprite(Cow)
cows = Group()
cows.add(cow)

lives = 3
running = True

# Main game loop
clock = pygame.time.Clock()
while running:
    ## Run handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #--------------    

    ## Event handling
    # Move paddle
    paddle.get_key_input()
    #-------------

    ## Game logic
    # Check if cow falls off
    for cow in cows:
        cow.handle_cliff_collision(cliffs)
        cow.handle_paddle_collision(paddle)
        cow.update()
        if cow.check_fall_off():
            lives -= 1
        if lives == 0:
            running = False

    #--------------

    # Draw elements
    screen.fill(LIGHT_BLUE)
    cliffs.draw(screen)
    cows.draw(screen)
    player.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
    #-------------
pygame.quit()

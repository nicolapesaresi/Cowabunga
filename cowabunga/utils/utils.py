import pygame

def create_sprite(sprite_class : pygame.sprite.Sprite, *args, **kwargs):
    """Create a sprite object with given arguments."""
    return sprite_class(*args, **kwargs)
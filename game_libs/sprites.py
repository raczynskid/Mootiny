import pygame
from game_libs.abstract_objects import Entity
from game_libs import game_objects

spr_index = {'cow': r'./assets/sprites/cow_static.png',
             'barn': r'./assets/sprites/barn.png'}


def load_image(name):
    """loads image to be used as sprite"""
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print('Cannot load image:', name)
        return None
    return image.convert(), image.get_rect()


class Sprite:
    """sprite object with preloaded image to pass to game object constructor"""

    def __init__(self, sprite_path):
        self.image, self.rect = load_image(sprite_path)
        self.image.set_colorkey((0, 0, 0))
        self.surface = pygame.display.get_surface()
        self.area = self.surface.get_rect()

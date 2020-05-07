import pygame
from game_libs import sprites
from game_libs import constants


class InterfaceBar:
    def __init__(self):
        self.__surface = pygame.display.get_surface()
        self.__sprite = sprites.Sprite(sprites.spr_index['interface'], color_key=(255, 0, 247))
        self.__position = (0, constants.Constants.WINDOW_HEIGHT - 200)
        self.__screen = pygame.display.get_surface()

    def get_position(self):
        """return interface bar position"""
        return self.__position

    def get_screen(self):
        """return interface bar surface"""
        return self.__screen

    def draw_self(self):
        """blit the sprite onto surface"""
        self.get_screen().blit(self.__sprite.image, (self.__position))

    def initialize_build_mode(self, type):
        return type


def check_build(mousePosition):
    x, y = mousePosition
    if x > 72 and x < 177 and y > 1077 and y < 1170:
        return 'barn'
    else:
        return None

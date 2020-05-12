import pygame

from game_libs import sprites
from game_libs.constants import Constants


class InterfaceBar:
    def __init__(self):
        self.__surface = pygame.display.get_surface()
        self.__sprite = sprites.Sprite(sprites.spr_index['interface'], color_key=(255, 0, 247))
        self.__position = (0, Constants.WINDOW_HEIGHT - 200)
        self.__screen = pygame.display.get_surface()
        self.__w1 = dict(Xleft=73,
                         Xright=73 + 105,
                         Ytop=Constants.WINDOW_HEIGHT - (24 + 105),
                         Ybottom=Constants.WINDOW_HEIGHT - 24)

    def get_position(self):
        """return interface bar position"""
        return self.__position

    def get_screen(self):
        """return interface bar surface"""
        return self.__screen

    def draw_self(self):
        """blit the sprite onto surface"""
        self.get_screen().blit(self.__sprite.image, (self.__position))

    def in_window1(self, coords):
        """return True if coordinates in first interface building window"""
        x, y = coords
        return self.__w1['Xleft'] < x < self.__w1['Xright'] and self.__w1['Ytop'] < y < self.__w1['Ybottom']

    def check_build(self, mouse_position):
        """return building type to create based on which interface bar window was clicked"""
        if self.in_window1(mouse_position):
            return 'barn'
        else:
            return None

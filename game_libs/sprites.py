import os
import sys
from random import randint

import pygame

from game_libs.constants import Constants


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return base_path + relative_path


def load_image(name):
    """loads image to be used as sprite"""
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print('Cannot load image:', name)
        return None
    return image.convert(), image.get_rect()


class Sprite:
    """base sprite object with preloaded image to pass to game object constructor"""

    def __init__(self, sprite_path, color_key=(0, 0, 0)):
        self.__color_key = color_key
        self.image, self.rect = load_image(sprite_path)
        self.image.set_colorkey(color_key)
        self.rotated_imgs = {
            'n': self.image,
            's': pygame.transform.rotate(self.image, 180),
            'e': pygame.transform.rotate(self.image, 270),
            'w': pygame.transform.rotate(self.image, 90),
            'ne': pygame.transform.rotate(self.image, 315),
            'nw': pygame.transform.rotate(self.image, 45),
            'sw': pygame.transform.rotate(self.image, 135),
            'es': pygame.transform.rotate(self.image, 225)}

        self.surface = pygame.display.get_surface()
        self.area = self.surface.get_rect()


    def change_color_key(self, rgb):
        """change the background color that is keyed on display"""
        self.image.set_colorkey(rgb)

    def reload_image(self, new_index):
        """reload with new image, same colorkey"""
        self.image, self.rect = load_image(new_index)
        self.image.set_colorkey(self.__color_key)

spr_index = {'cow': resource_path(r'\assets\sprites\cow_static.png'),
             'barn': resource_path(r'\assets\sprites\barn.png'),
             'barn_open': resource_path(r'\assets\sprites\barn_open.png'),
             'interface': resource_path(r'\assets\sprites\interface.png'),
             'grass1': resource_path(r'\assets\sprites\cows_grass.png'),
             'grass2': resource_path(r'\assets\sprites\cows_grass2.png'),
             'grass3': resource_path(r'\assets\sprites\cows_grass_flower1.png'),
             'cloud1': resource_path(r'\assets\sprites\cows_cloud.png')}

font_index = {'Amatic': resource_path(r'\assets\fonts\AmaticSC-Regular.ttf')}


class Grass:
    """non interactive sprite of random grass image"""

    def __init__(self):
        grass_sprites = [spr_index[spr] for spr in spr_index.keys() if 'grass' in spr]
        num = randint(0, len(grass_sprites) - 1)
        self.image, self.rect = load_image(grass_sprites[num])
        self.image.set_colorkey((255, 253, 252))
        self.surface = pygame.display.get_surface()
        self.position = (randint(0, Constants.WINDOW_WIDTH), randint(0, Constants.WINDOW_HEIGHT))

    def draw(self):
        self.surface.blit(self.image, self.position)


class Cloud:
    """non interactive sprite"""

    def __init__(self):
        self.image, self.rect = load_image(spr_index['cloud1'])
        self.image.set_colorkey((255, 255, 255))
        self.image.set_alpha(230)
        self.x = -500
        self.y = randint(50, Constants.WINDOW_HEIGHT - 350)
        self.speed = randint(1, 6)
        self.surface = pygame.display.get_surface()

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speed

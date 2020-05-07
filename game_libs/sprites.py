import pygame
import sys
import os


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
    """sprite object with preloaded image to pass to game object constructor"""

    def __init__(self, sprite_path, color_key=(0, 0, 0)):
        self.image, self.rect = load_image(sprite_path)
        self.image.set_colorkey(color_key)
        self.surface = pygame.display.get_surface()
        self.area = self.surface.get_rect()

    def change_color_key(self, rgb):
        self.image.set_colorkey(rgb)


spr_index = {'cow': resource_path(r'\assets\sprites\cow_static.png'),
             'barn': resource_path(r'\assets\sprites\barn.png'),
             'interface': resource_path(r'\assets\sprites\interface.png')}

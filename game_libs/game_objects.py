import pygame
from game_libs.constants import Constants
from game_libs.abstract_objects import Entity
from game_libs import sprites
from random import randint

class Building:
    def __init__(self, surface, position, hp, size, sprite):

        self.restrict_types(position[0], position[1], size, hp)
        self.__surface = surface
        self.__position = position
        self.__x = position[0]
        self.__y = position[1]
        self.__hp = hp
        self.__size = size
        self.__isDead = False
        self.__buildMode = False
        self.__active = False
        self.__sprite = sprite

    @staticmethod
    def restrict_types(*args):
        """
        static function in constructor, check if coordinates,
        size, hp are all of type int, else throw TypeError exception
        """
        if False in [isinstance(arg, int) for arg in args]:
            raise TypeError("size, position and hp must be integers")

    def get_surface(self):
        """return preset surface"""
        return self.__surface

    def set_surface(self, new_surface):
        """change the surface object should be drawn to"""
        self.__surface = new_surface

    def get_position(self):
        """return coordinates as tuple"""
        return self.__x, self.__y

    def set_position(self, x, y):
        """hard set coordinates"""
        self.__x, self.__y = x, y

    def is_build_mode(self):
        return self.__buildMode

    def set_build_mode(self, buildMode):
        self.__buildMode = buildMode

    def activate(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    def is_active(self):
        return self.__active

    def get_size(self):
        """return building size (width = size, height = 1/2 size)"""
        return self.__size

    def set_size(self, new_size):
        """change building size"""
        self.__size = new_size

    def build(self, mouse_pos):
        """WIP place on surface and make active"""
        if self.__buildMode:
            self.set_build_mode(False)
            x, y = mouse_pos
            self.set_position(x, y)
            self.activate()

    def get_hp(self):
        """return current hp of the building"""
        return self.__hp

    def set_hp(self, new_hp_value):
        """set statically new hp value"""
        self.__hp = new_hp_value

    def take_damage(self, damage):
        """lower hp by arg passed"""
        self.__hp -= damage
        if self.__hp <= 0:
            self.die()

    def repair(self, repair_value):
        """increase hp by repair value"""
        if not self.is_dead():
            self.__hp += repair_value

    def die(self):
        """set isDead state"""
        self.__isDead = True

    def is_dead(self):
        """return isDead state"""
        return self.__isDead

    def get_corners_coordinates(self, mouse_pos):
        """calculate corner positions of the building"""

        if self.is_build_mode():
            x, y = mouse_pos
        else:
            x, y = self.get_position()

        width = self.get_size()
        height = int(round(self.get_size() / 2))
        return {'NW': [x, y],
                'NE': [x + width, y],
                'SE': [x + width, y + height],
                'SW': [x, y + height]}

    def get_border_lines(self):
        """calculate hit box/draw box lines coordinates"""
        corners = self.get_corners_coordinates(None)
        lines = {'N': (corners['NW'], corners['NE']),
                 'E': (corners['NE'], corners['SE']),
                 'S': (corners['SE'], corners['SW']),
                 'W': (corners['SW'], corners['NW'])}

        return lines

    def draw_sprite(self, mouse_pos):
        pointlist = [t for t in self.get_corners_coordinates(mouse_pos).values()]
        # pygame.draw.lines(self.get_surface(), (255, 50, 50), True, pointlist, 5)
        self.get_surface().blit(self.__sprite.image, pointlist[0])



class Barn(Building):
    def __init__(self, position, production, production_interval):
        self.__production = production
        self.__production_interval = production_interval
        self.__production_queue = []
        self.__sprite = sprites.Sprite(sprites.spr_index['barn'])
        super().__init__(pygame.display.get_surface(), position, 100, 100, self.__sprite)

    def add_to_queue(self, item):
        """append new item to FIFO production queue"""
        self.__production_queue.append(item)

    def get_queue(self):
        """return current state of production queue"""
        return self.__production_queue

    def set_queue(self, item_list):
        """hard insert a queue"""
        self.__production_queue = item_list


class Cow(Entity):
    def __init__(self, position):
        Entity.__init__(self, pygame.display.get_surface(), position[0] + 10, position[1] + 32, 32, 'unit')
        self.__sprite = sprites.Sprite(sprites.spr_index['cow'])

    def draw_sprite(self):
        """blit the sprite onto surface"""
        x, y = self.get_position()
        self.get_surface().blit(self.__sprite.image, (x - 10, y - 32))

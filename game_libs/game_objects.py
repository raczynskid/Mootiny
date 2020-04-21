import pygame
from game_libs.constants import Constants
from random import randint


class Building:
    def __init__(self, surface, position, hp, size):
        self.__surface = surface
        self.__position = position
        self.__x = position[0]
        self.__y = position[1]
        self.__hp = hp
        self.__size = size
        self.__isDead = False

    def build(self):
        pass

    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp >= 0:
            self.die()

    def die(self):
        self.__isDead = True


class Barn(Building):
    def __init__(self, surface, position, production, production_interval):
        self.__production = production
        self.__production_interval = production_interval
        self.__production_queue = []
        super().__init__(surface, position, 100, (50, 50))

    def add_to_queue(self, item):
        self.__production_queue.append(item)

    def get_queue(self):
        return self.__production_queue

    def set_queue(self, item_list):
        self.__production_queue = item_list

    def draw(self):
        pass

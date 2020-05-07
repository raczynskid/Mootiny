from random import randint

from game_libs.game_objects import *


class EntityManager:
    """class to handle creating and destroying entities in game
    created entites should be added to EntityManager, and all events should be handled through it"""

    def __init__(self):
        """initialize empty list to store existing entities"""
        self.entities = []
        self.buildings = []

    def create_entity(self, entity):
        """add a new entity to the manager"""
        self.entities.append(entity)

    def destroy_entity(self, entity):
        """remove an entity from the manager"""
        self.entities.remove(entity)

    def create_building(self, building):
        """add a new building to the manager"""
        self.buildings.append(building)

    def destroy_building(self, building):
        """remove an building from the manager"""
        self.buildings.remove(building)

    def create_random_cow(self):
        """place a random cow somewhere on the map"""
        cow = Cow((randint(10, Constants.WINDOW_WIDTH - 10), randint(10, Constants.WINDOW_HEIGHT - 200)))
        cow.set_speed(10)
        cow.set_bounce(False)
        return cow

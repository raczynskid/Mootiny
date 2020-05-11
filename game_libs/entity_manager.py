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

    def check_for_new_orders(self, mouse_pos):
        """check if any buildings were clicked, if yes add to building queues"""
        mouse_x, mouse_y = mouse_pos
        for building in self.buildings:
            building_x, building_y = building.get_position()
            if (building_x + building.width) > mouse_x > building_x and (
                    building_y + building.length) > mouse_y > building_y:
                building.add_to_queue(1)

    def run_production_queues(self):
        for building in self.buildings:
            if building.run_queue():
                self.create_entity(building.production())

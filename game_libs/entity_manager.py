from game_libs.game_objects import *


class EntityManager:
    """class to handle creating and destroying entities in game
    created entites should be added to EntityManager, and all events should be handled through it"""

    def __init__(self):
        """initialize empty list to store existing entities"""
        self.entities = []
        self.buildings = []
        self.non_interactive = []

    def create_entity(self, entity):
        """add a new entity to the manager"""
        self.entities.append(entity)

    def destroy_entity(self, entity):
        """remove an entity from the manager"""
        self.entities.remove(entity)

    def create_non_interactive(self, entity):
        self.non_interactive.append(entity)

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
        self.create_entity(cow)

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

    def draw_non_interactives(self):
        for spr in self.non_interactive:
            spr.draw()

    def set_group_target(self, mg, target):
        """initiated by click event, set targets for all selected entities"""
        for e in [e for e in self.entities if e.get_selection()]:
            if target in mg.closed_list:
                return
            # create path of nodes coordinates (row, column) with a* alogorythm
            path = (mg.a_star(mg.get_row_column_by_pixel_coords(e.get_position()), target))
            # todo: type error here sometimes, not sure why
            # translate nodes coordinated into pixel coordinated
            pixel_path = [mg.get_pixel_coords_by_row_column(node) for node in path]
            # set the path for entity
            e.set_path(pixel_path)

    def move_and_hover(self, mouse_pos):
        """every frame check for action and apply movement and check for mouse hover to draw selection indicator"""
        for e in self.entities:
            e.move()
            e.hover(mouse_pos)

    def check_cow_collisions(self):
        """cow sprite collisions - probably to be deprecated in future"""
        cowlist = [cow for cow in self.entities if isinstance(cow, Cow)]
        for cow in cowlist:
            ix = cowlist.index(cow)
            for other_cow in cowlist[:ix] + cowlist[ix + 1:]:
                in_collision = cow.collide(other_cow.get_full_rect())
                if in_collision:
                    print("collide")

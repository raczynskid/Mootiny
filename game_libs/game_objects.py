from random import randint

import pygame

from game_libs import sprites
from game_libs.abstract_objects import Entity
from game_libs.constants import Constants


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
        self.__invalid = False

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

    def set_invalid_on(self):
        """turn invalid build position mode on"""
        self.__invalid = True

    def set_invalid_off(self):
        """turn invalid build position mode off"""
        self.__invalid = False

    def is_invalid(self):
        """check if position is invalid"""
        return self.__invalid

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
        if self.__buildMode and (self.is_invalid_placement(mouse_pos) or self.is_invalid()):
            pass
            # TODO; add sound effect
        elif self.__buildMode:
            self.set_build_mode(False)
            x, y = mouse_pos
            self.set_position(x, y)
            self.rect = pygame.Rect(x, y, self.get_size(), self.get_size())
            self.activate()

    def is_invalid_placement(self, mouse_pos):
        """in building mode check if near screen borders, if so, enable invalid mode """
        if self.is_build_mode():
            right_and_bottom_border = abs(Constants.WINDOW_WIDTH - mouse_pos[0]) < 150 or abs(
                Constants.WINDOW_HEIGHT - mouse_pos[1]) < 300
            left_and_top_border = abs(mouse_pos[0]) < 50 or abs(mouse_pos[1]) < 50
            if right_and_bottom_border or left_and_top_border:
                return True
        return False

    def is_build_collision(self, mouse_pos, other_buildings):
        """check if sprite in build mode collides with any other buildings, if so set invalid mode on"""
        mx, my = mouse_pos
        self.rect = pygame.Rect(mx, my, self.get_size(), self.get_size())
        for b in [b for b in other_buildings if b.is_active()]:
            if self.rect.colliderect(b.rect):
                self.set_invalid_on()
                return
        self.set_invalid_off()

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
        """blit the preloaded sprite onto surface"""
        pointlist = [t for t in self.get_corners_coordinates(mouse_pos).values()]
        self.get_surface().blit(self.__sprite.image, pointlist[0])
        if self.is_invalid_placement(mouse_pos) or self.is_invalid():
            self.set_invalid_on()
            self.draw_build_forbidden_mask(mouse_pos)
        else:
            self.set_invalid_off()

    def draw_build_forbidden_mask(self, mouse_pos):
        """draw transparent red mask over sprite if building is not allowed in build mode"""
        s = pygame.Surface((95, 95), pygame.SRCALPHA)
        s.fill((255, 0, 0, 90))
        self.get_surface().blit(s, mouse_pos)

class Barn(Building):
    def __init__(self, position, production_interval):
        self.__production_interval = production_interval * Constants.FRAMERATE
        self.__production_stop = self.__production_interval
        self.__production_queue = []
        self.__sprite = sprites.Sprite(sprites.spr_index['barn'])
        self.__open = False
        self.width = 92
        self.length = 92
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

    def get_stop_timer(self):
        """return the current time value of production stoppage timer"""
        return self.__production_stop

    def stop_timer_reset(self):
        """reset production stoppage timer to full production interval"""
        self.__production_stop = self.__production_interval

    def stop_timer_decrease(self):
        """decrease the production stoppage timer by 1"""
        self.__production_stop -= 1

    def door_open(self):
        """reload sprite as open doors, reflect in attribute"""
        self.__sprite.reload_image(sprites.spr_index['barn_open'])
        self.__open = True

    def door_close(self):
        """reload sprite as closed doors, reflect in attribute"""
        self.__sprite.reload_image(sprites.spr_index['barn'])
        self.__open = False

    def run_queue(self):
        """return boolean True if production should happen in current frame"""
        # if there are items in production queue
        if self.get_queue():
            # show how many left in queue
            self.draw_queue_counter()
            # reload sprite with open door image
            self.door_open()
            # check for stop timer being out
            if self.get_stop_timer() <= 0:
                # reset the timer
                self.stop_timer_reset()
                # pop first item in production stack
                self.__production_queue.pop(0)
                # return true to Entity manager to initiate production
                return True
            else:
                # if timer is not 0, decrease by 1
                self.stop_timer_decrease()
                # return false to entity manager so that unit is not created
                return False
        else:
            # if there are no items in production stack
            # reload sprite with closed door image if open
            if self.__open:
                self.door_close()
            # return false so that no new units are created
            return False

    def production(self):
        """return the default product (cow) and assign it initial random position around Barn"""
        x, y = self.get_position()
        prod = Cow((x + 30, y + 80))
        prod.set_target((x + randint(92, 200), y + randint(92, 200)))
        prod.set_speed(Constants.REGULAR_SPEED)
        return prod

    def draw_queue_counter(self):
        """show how many units left in production stack"""
        text = Constants.FONT.render(str(len(self.get_queue())), True, (255, 50, 0))
        self.get_surface().blit(text, self.get_position())


class Cow(Entity):
    def __init__(self, position):
        Entity.__init__(self, pygame.display.get_surface(), position[0] + 10, position[1] + 32, 32, 'unit')
        self.__sprite = sprites.Sprite(sprites.spr_index['cow'])
        self.__offsets = {'n': (10, 32),
                          's': (10, 32),
                          'w': (30, 15),
                          'e': (30, 15),
                          'ne': (30, 29),
                          'nw': (30, 29),
                          'es': (26, 30),
                          'sw': (26, 30)}

    def draw_sprite(self):
        """blit the sprite onto surface"""
        self.get_surface().blit(self.rotate(), self.position())

    def rotate(self):
        """choose from rotated sprites based on direction of movement"""
        direction = self.get_direction()
        try:
            return self.__sprite.rotated_imgs[direction]
        except KeyError:
            # anticipate where Entity attribute "direction" is not fulfilled
            return self.__sprite.image

    def position(self):
        """position sprite in relation to entity instance and offset rotation"""
        x, y = self.get_position()
        direction = self.get_direction()
        offset_x, offset_y = self.__offsets[direction]
        return x - offset_x, y - offset_y

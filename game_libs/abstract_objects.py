from random import randint

import pygame

from game_libs.constants import Constants


class Selection:
    """
    selection box based on dragging the cursor
    """

    def __init__(self, x, y):
        self.color = (255, 0, 144)
        self._x = x
        self._y = y
        self._current_x = x
        self._current_y = y
        self._fixed = None

    def update(self, current_x, current_y):
        """
        updates private class attributes with new values based on mouse position
        """
        self._current_x = current_x
        self._current_y = current_y

    def get_pos(self):
        """
        returns tuple of four (x,y) coordinates of selection box
        top right is always the fixed point (start of mousedrag)
        :return: tuple
        """
        bottom_left = (self._x, self._current_y)
        top_right = (self._current_x, self._y)
        bottom_right = (self._current_x, self._current_y)
        top_left = (self._x, self._y)
        return top_left, top_right, bottom_right, bottom_left

    def draw(self, surface):
        """
        draw the selection box to surface
        """
        pygame.draw.lines(surface, self.color, True, self.get_pos(), 5)


class Entity:
    """
    class for objects to interact with selection
    """

    def __init__(self, surface, x, y, size, entity_type):
        self._x = x
        self._y = y
        self.type = entity_type
        self.selected = False
        self._surface = surface
        self._size = size
        self._speed = 0
        self._direction = 'n'
        self._color = (0, 200, 255)
        self._bounce = False
        self.randomized = False
        self._target = None
        self._tempTarget = None
        self._hover = False
        self.initial_position = None

    def select(self):
        """switch selection on"""
        self.selected = True

    def deselect(self):
        """switch selection off"""
        self.selected = False

    def get_selection(self):
        """check if instance is in current selection"""
        return self.selected

    def get_surface(self):
        return self._surface

    def get_position(self):
        """get position as (x,y) tuple"""
        return self._x, self._y

    def set_position(self, position):
        """hard set object position to (x,y)"""
        self._x, self._y = position

    def get_speed(self):
        """return current speed of instance"""
        return self._speed

    def set_speed(self, speed):
        """set instance speed"""
        self._speed = speed

    def set_size(self, size):
        """set instance size"""
        self._size = size

    def get_size(self):
        """return instance size"""
        return self._size

    def set_bounce(self, bounce_on):
        """turn bounce behaviour on or off"""
        self._bounce = bounce_on

    def set_direction(self, direction):
        """set instance direction from N, S, W, E"""
        self._direction = direction

    def add_direction(self, direction):
        """add to direction string, valid inputs: n,s,w,e"""
        self._direction += direction

    def get_direction(self):
        """return instance direction as a set from string"""
        return self._direction

    def set_target(self, position):
        """set target position to (x,y) tuple"""
        self.initial_position = self.get_position()
        self._target = position

    def get_target(self):
        """return instance target, if not set return None"""
        return self._target

    def set_temporary_target(self, position):
        """
        set temporary target, executed in move() before regular _target,
        used for collisions (evade collided object)
        """
        self._tempTarget = position

    def get_temporary_target(self):
        """return instance temporary target, if not set return None"""
        return self._tempTarget


    def randomize_color(self):
        """set random rgb value for object"""
        self._color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def reset_color(self):
        """reset color to light blue"""
        self._color = (0, 200, 255)
        self.randomized = False

    def hover(self, mouse_pos):
        """check cursor coordinates against instance position"""
        if abs(self._x - mouse_pos[0]) < self._size and abs(self._y - mouse_pos[1]) < self._size:
            self._hover = True
        else:
            self._hover = False

    def get_hover(self):
        """check if instance is in mouse hover"""
        return self._hover

    def in_selection(self, selection):
        """determine if object is inside the passed selection box every time instance is drawn"""
        sw_select, nw_select, se_select, ne_select = (False, False, False, False)
        top_left, top_right, bottom_right, bottom_left = selection.get_pos()

        x = self._x
        y = self._y

        offset = self._size + 2

        # SW
        if top_left[0] > top_right[0] and bottom_left[1] > top_right[1]:
            sw = {
                "horizontal1": (x + offset < top_left[0] and y + offset < bottom_left[1]),
                "horizontal2": (y + offset > top_right[1]),
                "vertical": (x + offset > top_right[0] and y + offset < bottom_right[1])
            }
            if sw["horizontal1"] and sw["horizontal2"] and sw["vertical"]:
                sw_select = True
            else:
                sw_select = False

        # NW
        if top_left[0] > top_right[0] and bottom_left[1] < top_right[1]:
            nw = {
                "horizontal1": (x + offset < top_left[0] and y + offset > bottom_left[1]),
                "horizontal2": (y + offset < top_right[1]),
                "vertical": (x + offset > top_right[0] and y + offset > bottom_right[1])
            }
            if nw["horizontal1"] and nw["horizontal2"] and nw["vertical"]:
                nw_select = True
            else:
                nw_select = False

        # NE
        if top_left[0] < top_right[0] and bottom_left[1] < top_right[1]:
            ne = {
                "horizontal1": (x - offset > top_left[0] and y - offset > bottom_left[1]),
                "horizontal2": (y - offset < top_right[1]),
                "vertical": (x - offset < top_right[0] and y - offset > bottom_right[1])
            }
            if ne["horizontal1"] and ne["horizontal2"] and ne["vertical"]:
                ne_select = True
            else:
                ne_select = False

        # SE
        if top_left[0] < top_right[0] and bottom_left[1] > top_right[1]:
            se = {
                "horizontal1": (x - offset > top_left[0] and y - offset < bottom_left[1]),
                "horizontal2": (y - offset > top_right[1]),
                "vertical": (x - offset < top_right[0] and y - offset < bottom_right[1])
            }
            if se["horizontal1"] and se["horizontal2"] and se["vertical"]:
                se_select = True
            else:
                se_select = False

        if nw_select or sw_select or ne_select or se_select:
            self.select()
        else:
            self.deselect()

    def draw(self):
        """draw object, applying background if ._selected attribute is True"""
        if self.selected or self.get_hover():
            pygame.draw.circle(self._surface, (255, 0, 0), (self._x, self._y), self._size + 3)
        pygame.draw.circle(self._surface, self._color, (self._x, self._y), self._size)

    def draw_selection_indicator_only(self):
        """draw only the selection indicator circle if in selection"""
        if self.selected or self.get_hover():
            pygame.draw.circle(self._surface, (255, 0, 0), (self._x, self._y), self._size + 3, 3)

    def stop(self):
        """stop all movement"""
        self._speed = 0

    def move(self):
        """move the instance at set speed in constant direction"""
        if self.get_direction() is not None:
            directions = {
                "N": (0, -self.get_speed()),
                "S": (0, self.get_speed()),
                "W": (-self.get_speed(), 0),
                "E": (self.get_speed(), 0)
            }

            self._x += directions[self._direction][0]
            self._y += directions[self._direction][1]
            self.at_border()
        else:
            return None

    def goto_position(self):
        """move to specific coordinates at self._target"""
        if self.get_target() is not None:
            target_x, target_y = self.get_target()
            if self._x != target_x or self._y != target_y:
                self.set_direction('')

                # target north
                if self._y > target_y:
                    self._y -= self.get_speed()
                    self.add_direction('n')
                    if abs(self._x - target_x) > 100:
                        self.set_direction('n')

                # target east
                if self._x < target_x:
                    self._x += self.get_speed()
                    self.add_direction('e')
                    if abs(self._y - target_y) < 100:
                        self.set_direction('e')

                # target south
                if self._y < target_y:
                    self._y += self.get_speed()
                    if 'n' not in self.get_direction():
                        self.add_direction('s')
                        if abs(self._x - target_x) > 100:
                            self.set_direction('s')

                # target west
                if self._x > target_x:
                    self._x -= self.get_speed()
                    if 'e' not in self.get_direction():
                        self.add_direction('w')
                        if abs(self._y - target_y) < 100:
                            self.set_direction('w')

        self.at_border()

    def at_border(self):
        """defines behavior when hitting window borders"""
        x_borders_crossed = self._x > Constants.WINDOW_WIDTH or self._x < 0
        y_borders_crossed = self._y > Constants.WINDOW_HEIGHT or self._y < 0
        if x_borders_crossed or y_borders_crossed:
            if self._bounce:
                self.set_speed((self.get_speed()) * -1)
                self.reset_color()
            else:
                self.stop()
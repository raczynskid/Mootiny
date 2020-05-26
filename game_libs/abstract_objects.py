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
        self._hover = False
        self._current_path = []
        self._nodes = []
        self._current_node = None

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
        self._target = position

    def get_target(self):
        """return instance target, if not set return None"""
        return self._target

    def set_path(self, path):
        self._current_path = path

    def get_path(self):
        return self._current_path

    def is_path(self):
        if self._current_path:
            return True
        else:
            return False


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
        """move the instance along active path"""
        path = self.get_path()
        # check if active path exists
        if self.is_path():
            self.set_target(path[0])
            # exit function if on last node and reset path
            if path[0] == path[-1]:
                self.set_target(path[0])
                self.goto_position()
                self.set_path([])

            # if position is under 20 pixel distance from current node
            elif (abs(self._x - path[0][0]) < 20) & (abs(self._y - path[0][1]) < 20):
                # move to position
                self.goto_position()
                # drop current node from path
                self._current_path.pop(0)
                # set next node as target
                self.set_target(self.get_path()[0])
                # start moving
                self.goto_position()

            # if not on current node and not last node, keep moving
            else:
                self.goto_position()


    def goto_position(self):
        """move to specific coordinates at self._target"""
        if self.get_target() is not None:
            target_x, target_y = self.get_target()
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


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class MovementGrid:

    def __init__(self, w=Constants.WINDOW_WIDTH, h=Constants.WINDOW_HEIGHT, rsize=64):
        self.w = w
        self.h = h
        self.rsize = rsize
        self.surface = pygame.display.get_surface()
        self.xlines = self.make_xline_dict()
        self.ylines = self.make_yline_dict()
        self.grid = self.dict_of_squares()
        self.selected = []
        self.selection_block = False
        self.closed_list = []
        self.open_list = [sq for sq in self.grid.keys()]
        self.active_path = []

    def close_square(self, rc):
        try:
            r, c = rc
            ix = self.open_list.index((r, c))
            self.closed_list.append(self.open_list.pop(ix))
        except ValueError:
            print(rc, " already closed")
            pass

    def open_square(self, rc):
        r, c = rc
        ix = self.closed_list.index((r, c))
        self.open_list.append(self.closed_list.pop(ix))

    def make_xline_dict(self):
        """save list of all values at horizontal axis where gridlines start"""
        return [x for x in range(0, self.w + self.rsize, self.rsize)]

    def make_yline_dict(self):
        """save list of all values at vertical axis where gridlines start"""
        return [y for y in range(0, self.h + self.rsize, self.rsize)]

    def draw_grid(self):
        """draw gridlines based on xline and yline lists"""
        for xline in self.xlines:
            pygame.draw.line(self.surface, (255, 255, 255), (xline, 0), (xline, self.h))
        for yline in self.ylines:
            pygame.draw.line(self.surface, (255, 255, 255), (0, yline), (self.w, yline))

    def dict_of_squares(self):
        """
        create a dictionary where
        key = (row, column) and
        value = ((start x pixel, end x pixel)(start y pixel, end y pixel))
        :return a dictionary as {(row:column):((topLeft, topRight),(bottomLeft, bottomRight))}
        """
        row = 0
        column = 0
        d = {}
        self.xlines = self.make_xline_dict()
        self.ylines = self.make_yline_dict()

        # iterate through columns
        for xline in self.xlines[0:-1]:
            # iterate through lines
            for yline in self.ylines[0:-1]:
                # assign square dimensions to dictionary where keys are (row, column) tuples
                d[(row, column)] = (xline, xline + self.rsize), (yline, yline + self.rsize)
                # next row
                row += 1
            # next column
            column += 1
            # reset row
            row = 0
        return d

    def get_row_column_by_pixel_coords(self, pixel_coords):
        """return field row, column based on passed coordinates"""

        # loop thorugh all squares
        for k, v in self.grid.items():
            x1, x2 = v[0]
            y1, y2 = v[1]
            coord_x, coord_y = pixel_coords
            # check if passed x,y coordinates are inside any of the squares
            if (int(x1) <= int(coord_x) <= int(x2)) & (int(y1) <= int(coord_y) <= int(y2)):
                return k

    def get_pixel_coords_by_row_column(self, row_column, center=True):
        """return field row, column based on passed coordinates"""
        if center:
            return self.grid[row_column][0][0] + self.rsize // 2, self.grid[row_column][1][0] + self.rsize // 2
        else:
            return self.grid[row_column][0][0], self.grid[row_column][1][0]


    def highlight_square(self, coords):
        """
        returns the top left point coordinate of field that is established from passed coordinates
        """

        # color in every selected square
        for v in self.selected:
            x1, x2 = v[0]
            y1, y2 = v[1]
            pygame.draw.rect(self.surface, (150, 100, 220), pygame.Rect(x1, y1, self.rsize, self.rsize))

        v = self.grid[self.get_row_column_by_pixel_coords(coords)]
        sq_x, sq_y = v[0][0], v[1][0]
        pygame.draw.rect(self.surface, (240, 200, 255), pygame.Rect(sq_x, sq_y, self.rsize, self.rsize))

        return sq_x, sq_y

    def select_square(self, rc):
        """add square at coordintates (row, column) to selected list"""
        if self.grid[rc] not in self.selected:
            self.selected.append(self.grid[rc])
            self.selection_block = True

    def deselect_square(self, rc):
        """remove square at coordinates (row, column) from selected list"""
        if not self.selection_block:
            self.selected.pop((self.selected.index(self.grid[rc])))

    def get_neighbours(self, node):
        """return a list of all (row, column) coordinates that neighbour with argument coordinate"""
        r, c = node
        r -= 1
        c -= 1
        neighbours = [(r + x, c + y) for x in range(3) for y in range(3)]
        neighbours.pop(4)
        return neighbours

    def update_active_path(self, coords):
        self.active_path = self.a_star((0, 0), (self.get_row_column_by_pixel_coords(coords)))

    def a_star(self, start, end):
        open_list = []
        closed_list = []

        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list.append(start_node)

        while open_list:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for node_position in self.get_neighbours(current_node.position):

                # todo: Make sure not out of bounds
                pass

                # todo: make handler in case non-walkable passed as target

                # Make sure walkable terrain
                if node_position in self.closed_list:
                    break

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                if child in closed_list:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

import pygame


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

    def select(self):
        """switch selection on"""
        self.selected = True

    def deselect(self):
        """switch selection off"""
        self.selected = False

    def in_selection(self, selection):
        """determine if object is inside the passed selection box"""
        print(selection.get_pos())
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
        if self.selected:
            pygame.draw.circle(self._surface, (255, 0, 0), (self._x, self._y), self._size + 3)
        pygame.draw.circle(self._surface, (0, 200, 255), (self._x, self._y), self._size)

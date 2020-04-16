import pygame


class Selection:
    def __init__(self, x, y):
        self.color = (255, 0, 144)
        self._x = x
        self._y = y
        self._current_x = x
        self._current_y = y
        self._fixed = None

    def update(self, current_x, current_y):
        self._current_x = current_x
        self._current_y = current_y

    def get_pos(self):
        bottom_left = (self._x, self._current_y)
        top_right = (self._current_x, self._y)
        bottom_right = (self._current_x, self._current_y)
        top_left = (self._x, self._y)
        return top_left, top_right, bottom_right, bottom_left

    def draw(self, surface):
        pygame.draw.lines(surface, self.color, True, self.get_pos(), 5)

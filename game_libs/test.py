import unittest
from game_libs.game_objects import Building, Barn
from game_libs.abstract_objects import Selection, Entity, EntityGroup


class BuildingTests(unittest.TestCase):

    def test_if_building_position_is_tuple(self):
        test_b = Building(surface="surface", position=(10, 10), hp=100, size=20)
        self.assertTrue(test_b.get_position() == (10, 10))

    def test_x_position_is_integer(self):
        test_b = Building(surface="surface", position=(10, 10), hp=100, size=20)
        x_position = test_b.get_position()[0]
        self.assertTrue(isinstance(x_position, int))

    def test_y_position_is_integer(self):
        test_b = Building(surface="surface", position=(10, 10), hp=100, size=20)
        y_position = test_b.get_position()[1]
        self.assertTrue(isinstance(y_position, int))

    def test_x_position_is_float_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(2.3, 10), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_y_position_is_float_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(5, 2.9), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_x_position_is_string_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=('2', 10), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_y_position_is_string_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(5, '2'), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_hp__is_float_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(2.3, 10), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_size_is_float_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(5, 2.9), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_hp_is_string_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=('2', 10), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_size_is_string_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(5, '2'), hp=100, size=20)
        self.assertTrue(str(context.exception))

    def test_die_if_take_more_damaga_than_hp(self):
        test_b = Building(surface="surface", position=(10, 10), hp=100, size=20)
        test_b.take_damage(150)
        self.assertTrue(test_b.is_dead())

    def test_survive_if_take_less_damaga_than_hp(self):
        test_b = Building(surface="surface", position=(10, 10), hp=100, size=20)
        test_b.take_damage(50)
        self.assertFalse(test_b.is_dead())

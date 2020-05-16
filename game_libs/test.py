import unittest

from game_libs.game_objects import Building, Barn


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
            Building(surface="surface", position=(2.5, 10.5), hp=100, size=20)
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

    def test_hp_is_float_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(2.3, 10), hp=1.5, size=20)
        self.assertTrue(str(context.exception))

    def test_size_is_float_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(5, 2), hp=1, size=2.4)
        self.assertTrue(str(context.exception))

    def test_hp_is_string_throw_exception(self):
        with self.assertRaises(TypeError) as context:
            Building(surface="surface", position=(2, 10), hp='100', size=20)
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

    ### Barn specific
    def test_if_build_mode_off_by_default(self):
        self.assertFalse(Barn('surface', (0, 0), 'cow', 2).is_build_mode())

    def test_if_active_is_off_by_default(self):
        self.assertFalse(Barn('surface', (0, 0), 'cow', 2).is_active())

    def test_if_build_mode_turns_on_by_build_mode_on(self):
        b = Barn('surface', (0, 0), 'cow', 2)
        b.set_build_mode(True)
        self.assertTrue(b.is_build_mode())

    def test_if_active_mode_stays_off_by_build_mode_on(self):
        b = Barn('surface', (0, 0), 'cow', 2)
        b.set_build_mode(True)
        self.assertFalse(b.is_active())

    def test_if_mouse_coordinates_passed_to_draw_if_inactive_build_mode(self):
        b = Barn('surface', (0, 0), 'cow', 2)
        b.set_build_mode(True)
        test_mouse_position = (30, 30)
        corners = b.get_corners_coordinates(test_mouse_position)
        self.assertEqual(corners['NW'], list(test_mouse_position))

    def test_if_active_after_build(self):
        b = Barn('surface', (0, 0), 'cow', 2)
        b.set_build_mode(True)
        b.build()
        self.assertTrue(b.is_active())

    def test_if_default_coordinates_used_if_active(self):
        b = Barn('surface', (0, 0), 'cow', 2)
        b.set_build_mode(True)
        b.build()
        test_mouse_position = (30, 30)
        corners = b.get_corners_coordinates(test_mouse_position)
        self.assertEqual(corners['NW'], [0, 0])

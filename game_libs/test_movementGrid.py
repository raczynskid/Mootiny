from unittest import TestCase

import pygame

from game_libs.abstract_objects import MovementGrid


class TestMovementGrid(TestCase):
    def setUp(self):
        pygame.init()
        self.MG = MovementGrid()

    def test_make_xline_dict_at128x128(self):
        self.MG.w = 128
        self.MG.h = 128
        self.MG.rsize = 64

        self.assertEqual([0, 64, 128], self.MG.make_xline_dict())

    def test_make_xline_dict_at1600x1200(self):
        self.MG.w = 1600
        self.MG.h = 1200
        self.MG.rsize = 64
        res = [0, 64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216,
               1280, 1344, 1408, 1472, 1536, 1600]
        self.assertEqual(res, self.MG.make_xline_dict())

    def test_make_yline_dict_at128x128(self):
        self.MG.w = 128
        self.MG.h = 128
        self.MG.rsize = 64

        self.assertEqual([0, 64, 128], self.MG.make_yline_dict())

    def test_make_yline_dict_at1600x1200(self):
        self.MG.w = 1600
        self.MG.h = 1280
        self.MG.rsize = 64
        res = [0, 64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216,
               1280]
        self.assertEqual(res, self.MG.make_yline_dict())

    def test_dict_of_squares_at100x50_first(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.grid = self.MG.dict_of_squares()
        self.assertEqual(((0, 10), (0, 10)), self.MG.grid[(0, 0)])

    def test_dict_of_squares_at100x50_second(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.grid = self.MG.dict_of_squares()
        self.assertEqual(((10, 20), (0, 10)), self.MG.grid[(0, 1)])

    def test_get_row_column_by_pixel_coords(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.grid = self.MG.dict_of_squares()
        self.assertEqual((0, 3), self.MG.get_row_column_by_pixel_coords((33, 5)))

    def test_select_square(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.grid = self.MG.dict_of_squares()
        self.MG.select_square((0, 1))
        self.assertEqual(((10, 20), (0, 10)), self.MG.selected[-1])

    def test_deselect_square(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.grid = self.MG.dict_of_squares()
        self.MG.select_square((0, 1))
        self.MG.selection_block = False
        self.MG.deselect_square((0, 1))
        self.assertEqual([], self.MG.selected)

    def test_get_neighbours(self):
        self.MG.select_square((5, 5))
        self.assertEqual([(4, 4), (4, 5), (4, 6),
                          (5, 4), (5, 6),
                          (6, 4), (6, 5), (6, 6)], self.MG.get_neighbours((5, 5)))

    def test_open_list(self):
        mg = MovementGrid(10, 10, 5)
        self.assertEqual([(0, 0), (1, 0), (0, 1), (1, 1)], mg.open_list)

    def test_close_square(self):
        mg = MovementGrid(10, 10, 5)
        mg.close_square((1, 0))
        self.assertIn((1, 0), mg.closed_list)

    def test_close_and_open_square(self):
        mg = MovementGrid(10, 10, 5)
        mg.close_square((1, 0))
        mg.open_square((1, 0))
        self.assertIn((1, 0), mg.open_list)

    def test_a_star_straight_horizontal(self):
        mg = MovementGrid(10, 10, 5)
        self.assertEqual(mg.a_star((0, 0), (0, 5)), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)])

    def test_a_star_straight_vertical(self):
        mg = MovementGrid(10, 10, 5)
        self.assertEqual(mg.a_star((0, 0), (3, 0)), [(0, 0), (1, 0), (2, 0), (3, 0)])

    def test_a_star_straight_diagonal(self):
        mg = MovementGrid(10, 10, 5)
        self.assertEqual(mg.a_star((0, 0), (3, 3)), [(0, 0), (1, 1), (2, 2), (3, 3)])

    def test_a_star_straight_diagonal_reverse(self):
        mg = MovementGrid(10, 10, 5)
        self.assertEqual(mg.a_star((3, 3), (0, 0)), [(0, 0), (1, 1), (2, 2), (3, 3)][::-1])

    def test_a_star_straight_horizontal_large(self):
        mg = MovementGrid()
        self.assertEqual(mg.a_star((3, 3), (0, 0)), [(0, 0), (1, 1), (2, 2), (3, 3)][::-1])

    def test_a_star_straight_horizontal_large_with_closed_squares(self):
        mg = MovementGrid()
        self.assertEqual(mg.a_star((3, 3), (0, 0)), [(0, 0), (1, 1), (2, 2), (3, 3)][::-1])

    def test_get_pixel_coords_by_row_column(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.grid = self.MG.dict_of_squares()
        self.assertEqual((35, 5), self.MG.get_pixel_coords_by_row_column((0, 3)))

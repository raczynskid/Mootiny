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
        self.MG.d = self.MG.dict_of_squares()
        self.assertEqual(((0, 10), (0, 10)), self.MG.d[(0, 0)])

    def test_dict_of_squares_at100x50_second(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.d = self.MG.dict_of_squares()
        self.assertEqual(((10, 20), (0, 10)), self.MG.d[(0, 1)])

    def test_get_row_column_by_pixel_coords(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.d = self.MG.dict_of_squares()
        self.assertEqual((0, 3), self.MG.get_row_column_by_pixel_coords((33, 5)))

    def test_highlight_square(self):
        self.MG.w = 100
        self.MG.h = 50
        self.MG.rsize = 10
        self.MG.d = self.MG.dict_of_squares()
        self.assertEqual((0, 3), self.MG.highlight_square((0, 35)))

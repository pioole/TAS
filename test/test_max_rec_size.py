import unittest
import numpy as np

from src.MaxRecSize import Rectangle, Point, find_biggest_rectangle


class TestFindAllRectangles(unittest.TestCase):
    def test_find_all_rectangles(self):
        layer = np.asarray([[7., 0.], [0., 0.]])
        rect = find_biggest_rectangle(layer)

        self.assertEqual(rect.width * rect.height, 2)

    def test_find_all_rectangles_1(self):
        layer = np.asarray([[0., 0.], [0., 0.]])

        rect = find_biggest_rectangle(layer)

        self.assertEqual(rect.width * rect.height, 4)

    def test_find_all_rectangles_2(self):
        layer = np.asarray([[0., 0., 0.], [1., 0., 0.], [0., 0., 0.]])

        rect = find_biggest_rectangle(layer)

        self.assertEqual(rect.width * rect.height, 6)

    def test_find_all_rectangles_3(self):
        layer = np.asarray([[0., 0., 0.], [0., 0., 0.], [0., 0., 1.]])

        rect = find_biggest_rectangle(layer)

        self.assertEqual(rect.width * rect.height, 6)

    def test_find_all_rectangles_4(self):
        layer = np.asarray([[0., 0., 0.], [0., 0., 1.], [0., 0., 1.]])

        rect = find_biggest_rectangle(layer)

        self.assertEqual(rect.width * rect.height, 6)


if __name__ == '__main__':
    unittest.main()

import unittest

from src.MaxRecSize import max_size, max_rectangle_size, Rectangle, Point, find_biggest_rectangle


class TestMaxSize(unittest.TestCase):
    def test_max_size_1(self):
        self.assertEqual(max_size([[1, 1, 1], [0, 0, 0], [1, 1, 1]]), [(1, 3), 1, 0, 2])

    def test_max_size_2(self):
        self.assertEqual(max_size([[0, 0, 0], [1, 1, 1], [1, 1, 1]]), [(1, 3), 0, 0, 2])

    def test_max_size_3(self):
        self.assertEqual(max_size([[0, 0, 0], [0, 0, 0], [1, 1, 1]]), [(2, 3), 1, 0, 2])

    def test_max_size_4(self):
        self.assertEqual(max_size([[0, 0, 0], [1, 0, 0], [1, 1, 1]]), [(2, 2), 1, 1, 2])

    def test_max_size_5(self):
        self.assertEqual(max_size([[0, 0], [1, 1]]), [(1, 2), 0, 0, 1])


class TestMaxRectangleSize(unittest.TestCase):
    def test_max_rectangle_size_1(self):
        self.assertEqual(max_rectangle_size([1, 2, 6, 6, 3, 2], 0), Rectangle(top_left_point=Point(x=2, y=0), height=6, width=2))


class TestFindBiggestRectangle(unittest.TestCase):
    def test_find_biggest_rectangle_1(self):
        matrix = [[9, 0, 0, 0, 0, 19, 19, 19, 19, 20, 31, 31, 31, 31, 0, 34, 34, 37, 46, 46, 46, 53]]
        self.assertEqual(find_biggest_rectangle(matrix), Rectangle(top_left_point=Point(x=1, y=0), height=1, width=4))


if __name__ == '__main__':
    unittest.main()

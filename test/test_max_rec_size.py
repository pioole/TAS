import unittest

from src.MaxRecSize import max_size, max_rectangle_size


class TestMaxSize(unittest.TestCase):
    def test_max_size_1(self):
        self.assertEqual(max_size([[1, 1, 1], [0, 0, 0], [1, 1, 1]]), [(1, 3), 1, 0, 2])

    def test_max_size_2(self):
        self.assertEqual(max_size([[0, 0, 0], [1, 1, 1], [1, 1, 1]]), [(1, 3), 0, 0, -1])

    def test_max_size_3(self):
        self.assertEqual(max_size([[0, 0, 0], [0, 0, 0], [1, 1, 1]]), [(2, 3), 1, 0, 2])

    def test_max_size_4(self):
        self.assertEqual(max_size([[0, 0, 0], [1, 0, 0], [1, 1, 1]]), [(2, 2), 1, 1, 2])

    def test_max_size_5(self):
        self.assertEqual(max_size([[0, 0], [1, 1]]), [(1, 2), 0, 0, -1])


class TestMaxRectangleSize(unittest.TestCase):
    def test_max_rectangle_size_1(self):
        self.assertEqual(max_rectangle_size([1, 2, 6, 6, 3, 2], 0), (2, 6))


if __name__ == '__main__':
    unittest.main()

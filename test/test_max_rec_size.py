import unittest

from src.MaxRecSize import area, max_size


class TestArea(unittest.TestCase):
    def test_area_1(self):
        self.assertEqual(area((1, 2)), 2)

    def test_area_2(self):
        self.assertEqual(area((1, 2, 3)), 6)

    def test_area_3(self):
        self.assertEqual(area([1]), 1)


class TestMaxSize(unittest.TestCase):
    def test_max_size_1(self):
        self.assertEqual(max_size([[1, 1, 1], [0, 0, 0], [1, 1, 1]]), [(1, 3), 1, 0, 2])

    def test_max_size_2(self):
        self.assertEqual(max_size([[0, 0, 0], [1, 1, 1], [1, 1, 1]]), [(1, 3), 0, 0, -1])

    def test_max_size_3(self):
        self.assertEqual(max_size([[0, 0], [1, 1]]), [(1, 2), 0, 0, -1])


if __name__ == '__main__':
    unittest.main()

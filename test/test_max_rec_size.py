import unittest

from src.MaxRecSize import area


class TestArea(unittest.TestCase):
    def test_area_1(self):
        self.assertEqual(area((1, 2)), 2)

    def test_area_2(self):
        self.assertEqual(area((1, 2, 3)), 6)

    def test_area_3(self):
        self.assertEqual(area([1]), 1)


if __name__ == '__main__':
    unittest.main()

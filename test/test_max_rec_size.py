import unittest

from src.MaxRecSize import max_rectangle_size, Rectangle, Point, get_available_rectangles, rectangles_collide, \
    find_all_rectangles


class TestMaxRectangleSize(unittest.TestCase):
    def test_max_rectangle_size_1(self):
        self.assertEqual(max_rectangle_size([1, 2, 6, 6, 3, 2], 0), Rectangle(top_left_point=Point(x=2, y=0), height=6, width=2))


class TestGetAvailableRectangles(unittest.TestCase):
    def test_get_available_rectangles_1(self):
        histogram = [2, 1, 2]
        rectangles = get_available_rectangles(histogram, 0)
        self.assertEqual(max(rectangles, key=lambda rectangle: rectangle.height * rectangle.width), Rectangle(top_left_point=Point(x=0, y=0), height=1, width=3))


class TestFindAllRectangles(unittest.TestCase):
    def test_find_all_rectangles(self):
        layer = [[7., 0.], [0., 0.]]

        self.assertEqual(len(find_all_rectangles(layer)), 5)


class TestRectanglesCollide(unittest.TestCase):
    def test_rectangles_collide_1(self):
        rect1 = Rectangle(Point(0, 0), 2, 2)
        rect2 = Rectangle(Point(1, 1), 1, 1)
        self.assertTrue(rectangles_collide(rect1, rect2))

    def test_rectangles_collide_2(self):
        rect1 = Rectangle(Point(0, 0), 2, 2)
        rect2 = Rectangle(Point(2, 2), 1, 1)
        self.assertFalse(rectangles_collide(rect1, rect2))

    def test_rectangles_collide_3(self):
        rect1 = Rectangle(Point(1, 1), 1, 1)
        rect2 = Rectangle(Point(0, 0), 1, 1)
        self.assertFalse(rectangles_collide(rect1, rect2))

    def test_rectangles_collide_4(self):
        rect1 = Rectangle(Point(0, 0), 2, 2)
        rect2 = Rectangle(Point(1, 1), 1, 1)
        self.assertTrue(rectangles_collide(rect2, rect1))

if __name__ == '__main__':
    unittest.main()

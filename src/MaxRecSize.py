from collections import namedtuple

from src.Exceptions import NoRectangleException
from src.performance import perf

Point = namedtuple('Point', 'x y')
Rectangle = namedtuple('Rectangle', 'top_left_point height width')
Histogram = namedtuple('Histogram', 'value_list depth')


def find_biggest_rectangle(matrix):
    """
    find biggest rectangle in given matrix.
    :param matrix: Numpy 2D array
    :return:
    """
    def check_right(x, y):
        r_y = y
        try:
            while matrix[x][r_y] == 0:
                r_y += 1
        except IndexError:
            pass
        return Rectangle(Point(x, y), 1, r_y - y)

    def check_bottom(x, y):
        b_x = x
        try:
            while matrix[b_x][y] == 0:
                b_x += 1
        except IndexError:
            pass
        return Rectangle(Point(x, y), b_x - x, 1)

    def get_max_right(x, y):
        r_y = y
        try:
            while matrix[x][r_y] == 0:
                r_y += 1
        except IndexError:
            pass
        return r_y - 1

    def get_max_bottom(x, y):
        b_x = x
        try:
            while matrix[b_x][y] == 0:
                b_x += 1
        except IndexError:
            pass
        return b_x - 1

    def check_diagonal(x, y, max_bottom=None, max_right=None):
        if max_right is None and max_bottom is None:
            max_right = get_max_right(x, y)
            max_bottom = get_max_bottom(x, y)

        rectangles = []

        if matrix[x:max_bottom + 1, y:max_right + 1].sum() == 0:
            rectangles.append(Rectangle(Point(x, y), max_bottom - x + 1, max_right - y + 1))
        else:
            for bottom in xrange(x + 1, max_bottom + 1):
                for right in xrange(y + 1, max_right + 1):
                    if matrix[x:bottom + 1, y:right + 1].sum() == 0:
                        rectangles.append(Rectangle(Point(x, y), bottom - x + 1, right - y + 1))

        return rectangles

    rectangles = []
    r_done = False
    b_done = False
    d_r_done = False
    d_b_done = False

    for x in xrange(matrix.shape[0]):
        for y in xrange(matrix.shape[1]):
            if matrix[x][y] == 0:
                if not r_done:
                    rectangles.append(check_right(x, y))
                    r_done = True
            else:
                r_done = False
        r_done = False

    for y in xrange(matrix.shape[1]):
        for x in xrange(matrix.shape[0]):
            if matrix[x][y] == 0:
                if not b_done:
                    rectangles.append(check_bottom(x, y))
                    b_done = True
            else:
                b_done = False
        b_done = False

    for x in xrange(matrix.shape[0]):
        for y in xrange(matrix.shape[1]):
            if matrix[x][y] == 0:
                if not d_r_done:
                    rectangles.extend(check_diagonal(x, y))
                    d_r_done = True
            else:
                d_r_done = False
        d_r_done = False

    for y in xrange(matrix.shape[1]):
        for x in xrange(matrix.shape[0]):
            if matrix[x][y] == 0:
                if not d_b_done:
                    rectangles.extend(check_diagonal(x, y))
                    d_b_done = True
            else:
                d_b_done = False
        d_b_done = False

    try:
        return max(rectangles, key=lambda rect: rect.width * rect.height)
    except ValueError:
        raise NoRectangleException




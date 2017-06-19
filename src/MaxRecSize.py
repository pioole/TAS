from collections import namedtuple

from src.performance import perf

Point = namedtuple('Point', 'x y')
Rectangle = namedtuple('Rectangle', 'top_left_point height width')
Histogram = namedtuple('Histogram', 'value_list depth')


def find_all_rectangles(matrix, empty_value=0):
    """
    returns biggest available colliding rectangles from given matrix
    :param matrix: np array
    :param empty_value: Int
    :return: [Rectangle]
    """
    histograms = []

    matrix_height = len(matrix)
    matrix_width = len(matrix[0])

    for depth in xrange(matrix_height):

        histogram = [0] * matrix_width

        for row_num in reversed(xrange(depth, matrix_height)):
            for col_num in xrange(matrix_width):

                if matrix[row_num][col_num] == empty_value:
                    histogram[col_num] += 1
                else:
                    histogram[col_num] = 0

        histograms.append(Histogram(histogram, depth))

    rectangles = []
    for histogram in histograms:
        rectangle_list = get_available_rectangles(histogram.value_list, histogram.depth)
        rectangles.extend(rectangle_list)

    return rectangles


def max_rectangle_size(histogram, depth):
    rectangles = get_available_rectangles(histogram, depth)
    return max(rectangles, key=lambda rectangle: rectangle.height * rectangle.width)


def get_available_rectangles(histogram, depth):
    """
    returns biggest available colliding rectangles from given histogram
    :param histogram: Histogram
    :param depth: Int
    :return: [Rectangle]
    """
    indices = []
    for area_length in xrange(1, len(histogram)):
        for start_index in xrange(len(histogram)-area_length):
            indices.append((start_index, start_index + area_length))

    rectangles = []

    for area_length in xrange(0, len(histogram)):  # single columns
        h = histogram[area_length]
        for x_h in xrange(1, h + 1):
            rectangles.append(Rectangle(Point(area_length, depth), x_h, 1))

    for hist_part in indices:  # rects between given indices
        common_min = min([histogram[x] for x in xrange(hist_part[0], hist_part[1] + 1)])
        w = hist_part[1] - hist_part[0] + 1

        if w > 0:
            for x_h in xrange(1, common_min + 1):
                rectangles.append(Rectangle(Point(hist_part[0], depth), x_h, w))

    return rectangles


def overlapping_rectangle_cleaner(rectangle_list):
    biggest_rectangles = []
    while len(rectangle_list) > 0:
        biggest_rectangle = max(rectangle_list, key=lambda rect: rect.width * rect.height)
        rectangle_list = filter(lambda rect: not rectangles_collide(biggest_rectangle, rect), rectangle_list)
        biggest_rectangles.append(biggest_rectangle)
    return biggest_rectangles


def rectangles_collide(rect1, rect2):
    rect1_top_left = rect1.top_left_point
    rect1_top_right = Point(rect1.top_left_point.x + rect1.width - 1, rect1.top_left_point.y)
    rect1_bottom_left = Point(rect1.top_left_point.x, rect1.top_left_point.y + rect1.height - 1)
    rect1_bottom_right = Point(rect1.top_left_point.x + rect1.width - 1, rect1.top_left_point.y + rect1.height - 1)

    rect1_vertices_list = [rect1_top_left, rect1_top_right, rect1_bottom_left, rect1_bottom_right]

    for vertex in rect1_vertices_list:
        if rect2.top_left_point.x <= vertex.x <= rect2.top_left_point.x + rect2.width - 1 and \
           rect2.top_left_point.y <= vertex.y <= rect2.top_left_point.y + rect2.height - 1:
            return True
    return False

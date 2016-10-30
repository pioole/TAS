from collections import namedtuple


Point = namedtuple('Point', 'x y')
Rectangle = namedtuple('Rectangle', 'top_left_point height width')
Histogram = namedtuple('Histogram', 'value_list depth')


def max_size(matrix, empty_value=0):
    max_rectangle = find_biggest_rectangle(matrix, empty_value)
    return [(max_rectangle.height, max_rectangle.width), max_rectangle.top_left_point.y + max_rectangle.height - 1, max_rectangle.top_left_point.x, max_rectangle.top_left_point.x + max_rectangle.width -1]


def find_biggest_rectangle(matrix, empty_value=0):

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
        rectangle = max_rectangle_size(histogram.value_list, histogram.depth)
        rectangles.append(rectangle)

    return max(rectangles, key=lambda rectangle: rectangle.height * rectangle.width)


def max_rectangle_size(histogram, depth):
    indices = []
    for area_length in xrange(0, len(histogram)):
        for start_index in xrange(len(histogram)-area_length):
            indices.append((start_index, start_index + area_length))

    rectangles = []

    for hist_part in indices:
        h1 = histogram[hist_part[0]]
        h2 = histogram[hist_part[1]]
        w = hist_part[1] - hist_part[0] + 1

        rectangles.append(Rectangle(Point(hist_part[0], depth), h1, 1))
        rectangles.append(Rectangle(Point(hist_part[1], depth), h2, 1))
        rectangles.append(Rectangle(Point(hist_part[0], depth), min(h1, h2), w))

    max_rectangle = max(rectangles, key=lambda rectangle: rectangle.height * rectangle.width)
    return max_rectangle


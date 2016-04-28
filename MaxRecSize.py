from collections import namedtuple
from operator import mul

Info = namedtuple('Info', 'start height')

startcolcount = 0
endcolcount = 0


def max_size(mat, value=0):
    """Find height, width of the largest rectangle containing all `value`'s."""
    global startcolcount
    global endcolcount
    it = iter(mat)
    hist = [(el == value) for el in next(it, [])]
    # print hist
    max_size = max_rectangle_size(hist)
    # print max_size
    rowcount = 0
    max_at_row = 0
    max_at_col_start = 0
    max_at_col_end = 0
    for row in it:
        rowcount += 1
        hist = [(1 + h) if el == value else 0 for h, el in zip(hist, row)]
        # print "hist:"+str(hist)
        # print max_size
        # print max_rectangle_size(hist)

        if max(max_size, max_rectangle_size(hist), key=area) == max_rectangle_size(hist):
            # print "it"
            max_size = max(max_size, max_rectangle_size(hist), key=area)
            max_at_row = rowcount
            max_at_col_start = startcolcount
            max_at_col_end = endcolcount

    return [max_size, max_at_row, max_at_col_start, max_at_col_end - 1]


def max_rectangle_size(histogram):
    """Find height, width of the largest rectangle that fits entirely under
    the histogram.
    """
    global startcolcount
    global endcolcount
    stack = []
    top = lambda: stack[-1]
    max_size = (0, 0)  # height, width of the largest rectangle
    pos = 0  # current position in the histogram
    for pos, height in enumerate(histogram):
        start = pos  # position where rectangle starts
        while True:
            if not stack or height > top().height:
                stack.append(Info(start, height))  # push
            elif stack and height < top().height:
                if max(max_size, (top().height, (pos - top().start)), key=area) == (top().height, (pos - top().start)):
                    max_size = max(max_size, (top().height, (pos - top().start)), key=area)
                    # print max_size
                    startcolcount = top().start
                    # print "beforeloopstart"+str(startcolcount)
                    endcolcount = pos
                    # print "beforeloopend"+str(endcolcount)
                start, _ = stack.pop()
                continue
            break  # height == top().height goes here

    pos += 1
    for start, height in stack:
        if max(max_size, (height, (pos - start)), key=area) == (height, (pos - start)):
            max_size = max(max_size, (height, (pos - start)), key=area)
            startcolcount = start
            # print start
            endcolcount = pos
            # print pos
    return max_size


def area(size):
    return reduce(mul, size)


def main():
    result = max_size([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1]])
    print result[0][2]


if __name__ == "__main__":
    main()

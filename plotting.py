from matplotlib.pyplot import plot, draw, show
import time


class Plotter:
    def __init__(self):
        self.counter = 0

    def plot(self, value):
        print 'plotting value ' + str(value) + ' ' + str(self.counter)
        print plot([self.counter], [value], 'ro')
        self.counter += 1
        draw()
        show(block=False)

    def preserve_window(self):
        show()




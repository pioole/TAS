from matplotlib.pyplot import plot, draw, show, figure
import time


class Plotter:
    def __init__(self):
        self.counter = 0

    def plot(self, value):
        figure(1)
        plot([self.counter], [value], 'ro')
        self.counter += 1
        draw()
        show(block=False)

    def preserve_window(self):
        show()




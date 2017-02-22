from matplotlib.pyplot import plot, draw, show, figure
import time


class Plotter:
    def __init__(self, figure_num):
        self.counter = 0
        self.figure_num = figure_num

    def plot(self, value):
        figure(self.figure_num)
        plot([self.counter], [value], 'ro')
        self.counter += 1
        draw()
        show(block=False)

    def preserve_window(self):
        show()




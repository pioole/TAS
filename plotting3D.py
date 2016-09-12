import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show, draw, cla


colour_map = {
    0: 'b',
    1: 'g',
    2: 'r',
    3: 'c',
    4: 'm',
    5: 'y',
    6: 'k',
}


class Plotter3D:
    def __init__(self):
        self.fig = figure(2)
        self.ax = self.fig.add_subplot(111, projection='3d')

    def plot(self, plot_points):
        figure(2)
        cla()
        for plot_group in plot_points:
            xs, ys, zs, colour_seed = plot_group
            colour_number = colour_seed % len(colour_map)
            colour = colour_map[colour_number]
            self.ax.scatter(xs, ys, zs, c=colour, marker='o')

        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')

        draw()
        show(block=False)

    def preserve_window(self):
        show()


#
# plt = Plotter3D()
# plt.plot(1, 2, 3)
# from plotting import Plotter
# plt1 = Plotter()
# plt1.plot(1)
# import time
# time.sleep(4)
# plt.plot(4, 5, 6)
# plt1.plot(3)
#
# plt1.preserve_window()
#
# plt.preserve_window()
#

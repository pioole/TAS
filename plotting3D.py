import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure, show, draw, cla


class Plotter3D:
    def __init__(self):
        self.fig = figure(2)
        self.ax = self.fig.add_subplot(111, projection='3d')

    def plot(self, xs, ys, zs):
        figure(2)
        cla()
        self.ax.scatter(xs, ys, zs, c='r', marker='o')

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

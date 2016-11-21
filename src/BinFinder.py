import numpy as np

from src.Bin import Bin
from src.Exceptions import NoBinsAvailableException
from src.MaxRecSize import find_biggest_rectangle
from src.geometry_utils import Point3D


class BinFinder(object):
    def __init__(self, cluster_side_length):
        self.cluster_side_length = cluster_side_length

    def get_available_bins(self, node_matrix):
        node_matrix_mutable = np.copy(node_matrix)

        bin_found = True
        bin_list = []

        while bin_found:
            try:
                print 'searching for bin..'
                new_bin = self.get_biggest_bin_in_matrix(node_matrix_mutable)
                print 'found: {}'.format(new_bin)
                bin_list.append(new_bin)
                BinFinder.mark_space_as_used(node_matrix_mutable, new_bin)
            except NoBinsAvailableException:
                bin_found = False

        return bin_list

    @staticmethod
    def mark_space_as_used(matrix, bin_):
        """
        fills the space taken by the given bin in given matrix (in situ)
        :param matrix: 3d np array
        :param bin_: Bin
        :return: None
        """
        used_nodes = bin_.generate_point_nodes()
        for node in used_nodes:
                matrix[node.x][node.y][node.z] = 1

    def get_biggest_bin_in_matrix(self, matrix):
        """
        returns the biggest bin available in given matrix
        :param matrix: 3d np array
        :return: Bin
        """
        available_bins = []
        for x in xrange(0, self.cluster_side_length):
            for y in xrange(x, self.cluster_side_length):
                available_bins.append(BinFinder.get_biggest_bin_between_layers(self, x, y, matrix))
        biggest_bin = max(available_bins, key=lambda bin_: bin_.get_size())
        if biggest_bin.get_size() == 0:
            raise NoBinsAvailableException
        return biggest_bin

    def get_biggest_bin_between_layers(self, bottom_layer, top_layer, matrix):
        """
        finds and creates a biggest bin in given matrix which fits between top and bottom layer inclusive.
        the returned bin must 'touch' both top and bottom layer
        :param top_layer: Int
        :param bottom_layer: Int
        :param matrix: 3d np array
        :return: Bin
        """
        combined_layer = self.combine_layers(bottom_layer, top_layer, matrix)
        biggest_rectangle = find_biggest_rectangle(combined_layer)
        anchor_point = Point3D(bottom_layer,
                               biggest_rectangle.top_left_point.y,
                               biggest_rectangle.top_left_point.x)
        biggest_bin = Bin(anchor_point, top_layer - bottom_layer + 1, biggest_rectangle.height, biggest_rectangle.width)
        return biggest_bin

    def combine_layers(self, bottom_layer, top_layer, matrix):
        """
        returns a 2d numpy array with '0' value in places which are free in all of the 2d arrays from 'bottom layer' to
        'top layer' according to z axis
        :param top_layer: Int
        :param bottom_layer: Int
        :param matrix: 3d np array
        :return: 2d np array
        """
        layer_list = np.split(matrix, self.cluster_side_length)
        layers_to_combine = layer_list[bottom_layer:top_layer + 1]
        return np.sum(layers_to_combine, axis=0)[0]

import numpy as np
import logging


from src.Bin import Bin
from src.Exceptions import NoBinsAvailableException, NoRectangleException
from src.MaxRecSize import find_biggest_rectangle
from src.geometry_utils import Point3D
from performance import perf


MINIMAL_BIN_SIZE = 1


class BinFinder(object):
    def __init__(self, cluster_side_length, minimal_bin_size=MINIMAL_BIN_SIZE):
        """
        creates a new BinFinder with cluster of equal sizes according to all axis (cube).
        :param cluster_side_length:  Int
        :return: BinFinder
        """
        self.cluster_side_length = cluster_side_length
        self.minimal_bin_size = minimal_bin_size

    @perf
    def get_available_bins(self, node_matrix):
        """
        returns the list of all (non colliding) bins available in given matrix.
        :param node_matrix: 3d np array
        :return: [Bin]
        """
        node_matrix_mutable = np.copy(node_matrix)
        bin_list_end = []

        chance = True
        while chance:
            try:
                bin_raw = self.get_biggest_bin_in_matrix(node_matrix_mutable)
                if bin_raw.get_size() >= self.minimal_bin_size:
                    for node in bin_raw.generate_point_nodes():
                        node_matrix_mutable[node.x][node.y][node.z] = 1
                bin_list_end.append(bin_raw)
            except NoBinsAvailableException:
                chance = False

        logging.debug('No of bins found: {}'.format(len(bin_list_end)))

        return bin_list_end

    def get_biggest_bin_in_matrix(self, matrix):
        """
        returns biggest bin available in given matrix
        :param matrix: 3d np array
        :return: Bin
        """
        available_bins = []
        layer_list = np.split(matrix, self.cluster_side_length)

        for x in xrange(0, self.cluster_side_length):
            for y in xrange(x, self.cluster_side_length):
                try:
                    available_bins.append(BinFinder.get_biggest_bin_between_layers(self, x, y, layer_list))
                except NoBinsAvailableException:
                    pass

        try:
            return max(available_bins, key=lambda bin_: bin_.get_size())
        except ValueError:
            raise NoBinsAvailableException

    def get_biggest_bin_between_layers(self, bottom_layer, top_layer, layer_list):
        """
        returns biggest bin in given matrix which fits between top and bottom layer inclusive.
        the returned bins must 'touch' both top and bottom layer
        :param top_layer: Int
        :param bottom_layer: Int
        :param matrix: 3d np array
        :return: [Bin]
        """
        combined_layer = self.combine_layers(bottom_layer, top_layer, layer_list)
        try:
            rect = find_biggest_rectangle(combined_layer)
            bin_list = []
            anchor_point = Point3D(bottom_layer,
                                   rect.top_left_point.x,
                                   rect.top_left_point.y)
            bin = Bin(anchor_point, top_layer - bottom_layer + 1, rect.height, rect.width)
            bin_list.append(bin)

            return max(bin_list, key=lambda bin_: bin_.get_size())
        except (ValueError, NoRectangleException):
            raise NoBinsAvailableException

    def combine_layers(self, bottom_layer, top_layer, layer_list):
        """
        returns a 2d numpy array with '0' value in places which are free in all of the 2d arrays from 'bottom layer' to
        'top layer' according to z axis
        :param top_layer: Int
        :param bottom_layer: Int
        :param matrix: 3d np array
        :return: 2d np array
        """
        layers_to_combine = layer_list[bottom_layer:top_layer + 1]
        return np.sum(layers_to_combine, axis=0)[0]

    @staticmethod
    @perf
    def overlapping_bin_cleaner(bin_list):
        """
        gets a list of bins and returns a list of biggest non-colliding bins. Bins shall be of size greater than 0.
        :param bin_list: [Bin]
        :return: [Bin]
        """
        biggest_bins = []
        while len(bin_list) > 0:
            biggest_bin = max(bin_list, key=lambda bin_: bin_.get_size())
            bin_list = filter(lambda bin_: not BinFinder.bins_collide(biggest_bin, bin_), bin_list)
            biggest_bins.append(biggest_bin)
        return biggest_bins

    @staticmethod
    def bins_collide(bin1, bin2):
        """
        returns information if two given bins collide with each other.
        :param bin1: Bin
        :param bin2: Bin
        :return: Boolean
        """
        nodes_1 = bin1.generate_point_nodes()
        nodes_2 = bin2.generate_point_nodes()
        return not set(nodes_1).isdisjoint(nodes_2)


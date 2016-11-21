import unittest
import numpy as np

from src.Bin import Bin
from src.BinFinder import BinFinder
from src.Exceptions import NoBinsAvailableException
from src.geometry_utils import Point3D


class TestCombineLayers(unittest.TestCase):
    def test_combine_layers_1(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        desired_output = np.array([[2, 2, 2],
                                   [2, 0, 2],
                                   [2, 2, 2]])

        output_ = bin_finder.combine_layers(0, 2, input_)

        self.assertTrue(np.array_equal(desired_output, output_))

    def test_combine_layers_2(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        desired_output = np.array([[1, 1, 1],
                                   [1, 0, 1],
                                   [1, 1, 1]])

        output_ = bin_finder.combine_layers(0, 1, input_)

        self.assertTrue(np.array_equal(desired_output, output_))


class TestGetBiggestBinBetweenLayers(unittest.TestCase):
    def test_get_biggest_bin_between_layers_1(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        desired_output = Bin(Point3D(0, 1, 1), 3, 1, 1)

        output_ = bin_finder.get_biggest_bin_between_layers(0, 2, input_)

        self.assertEqual(desired_output, output_)

    def test_get_biggest_bin_between_layers_2(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        desired_output = Bin(Point3D(1, 0, 0), 1, 3, 3)

        output_ = bin_finder.get_biggest_bin_between_layers(1, 1, input_)

        self.assertEqual(desired_output, output_)


class TestGetBiggestBinInMatrix(unittest.TestCase):
    def test_get_biggest_bin_in_matrix_1(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        desired_output = Bin(Point3D(1, 0, 0), 1, 3, 3)

        output_ = bin_finder.get_biggest_bin_in_matrix(input_)

        self.assertEqual(desired_output, output_)

    def test_get_biggest_bin_in_matrix_2(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]],
                           [[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]],
                           [[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]]])

        self.assertRaises(NoBinsAvailableException, bin_finder.get_biggest_bin_in_matrix, input_)


class TestGetAvailableBins(unittest.TestCase):
    def test_get_available_bins_1(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        output_ = bin_finder.get_available_bins(input_)

        desired_output = [Bin(Point3D(x=1, y=0, z=0), 1, 3, 3),
                          Bin(Point3D(x=0, y=1, z=1), 1, 1, 1),
                          Bin(Point3D(x=2, y=1, z=1), 1, 1, 1)]

        self.assertEqual(output_, desired_output)

    def test_get_available_bins_2(self):
        bin_finder = BinFinder(3)

        input_ = np.array([[[1, 1, 0],
                            [1, 0, 1],
                            [1, 1, 1]],
                           [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                           [[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]]])

        output_ = bin_finder.get_available_bins(input_)

        desired_output = [Bin(Point3D(x=1, y=0, z=0), 1, 3, 3),
                          Bin(Point3D(x=2, y=1, z=1), 1, 1, 1),
                          Bin(Point3D(x=0, y=1, z=1), 1, 1, 1),
                          Bin(Point3D(x=0, y=0, z=2), 1, 1, 1)]

        self.assertEqual(set(output_), set(desired_output))


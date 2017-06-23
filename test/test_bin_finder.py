import unittest
import numpy as np
import logging

from src.Bin import Bin
from src.BinFinder import BinFinder
from src.geometry_utils import Point3D
from src.performance import perf


class TestCombineLayers(unittest.TestCase):
    def test_combine_layers_1(self):
        bin_finder = BinFinder(3, minimal_bin_size=0)

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

        input_ = np.split(input_, 3)

        output_ = bin_finder.combine_layers(0, 2, input_)

        self.assertTrue(np.array_equal(desired_output, output_))

    def test_combine_layers_2(self):
        bin_finder = BinFinder(3, minimal_bin_size=0)

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

        input_ = np.split(input_, 3)

        output_ = bin_finder.combine_layers(0, 1, input_)

        self.assertTrue(np.array_equal(desired_output, output_))


class TestGetAvailableBins(unittest.TestCase):
    def test_get_available_bins_1(self):
        bin_finder = BinFinder(3, minimal_bin_size=0)

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
        bin_finder = BinFinder(3, minimal_bin_size=0)

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

    def test_get_available_bins_3(self):
        bin_finder = BinFinder(1, minimal_bin_size=0)

        input_ = np.array([[[7.,  0.],
                            [0.,  0.]],
                           ])

        output_ = bin_finder.get_available_bins(input_)

        self.assertEqual(sum([bin_.get_size() for bin_ in output_]), 3)

    def test_get_available_bins_4(self):
        bin_finder = BinFinder(2, minimal_bin_size=0)

        input_ = np.array([[[7.,  0.],
                            [0.,  0.]],
                           [[0.,  0.],
                            [0.,  0.]]])

        output_ = bin_finder.get_available_bins(input_)

        self.assertEqual(sum([bin_.get_size() for bin_ in output_]), 7)

    def test_get_available_bins_5(self):
        bin_finder = BinFinder(3, minimal_bin_size=0)

        input_ = np.array([[[0., 0., 0.],
                            [0., 0., 0.],
                            [0., 6., 0.]],
                           [[0., 0., 0.],
                            [0., 0., 0.],
                            [0., 0., 0.]],
                           [[0., 0., 0.],
                            [0., 0., 0.],
                            [0., 0., 0.]]])

        output_ = bin_finder.get_available_bins(input_)

        self.assertEqual(sum([bin_.get_size() for bin_ in output_]), 26)

    def test_get_available_bins_6(self):
        bin_finder = BinFinder(3, minimal_bin_size=0)

        input_ = np.array([[[1., 0., 0.],
                            [0., 0., 0.],
                            [0., 0., 0.]],
                           [[0., 0., 0.],
                            [0., 1., 0.],
                            [0., 0., 0.]],
                           [[0., 0., 0.],
                            [0., 0., 0.],
                            [0., 0., 0.]]])

        output_ = bin_finder.get_available_bins(input_)

        self.assertEqual(sum([bin_.get_size() for bin_ in output_]), 25)

    @perf
    def test_get_available_bins_7(self):
        side = 24

        bin_finder = BinFinder(side, minimal_bin_size=0)

        input_ = np.zeros((side, side, side))

        output_ = bin_finder.get_available_bins(input_)

        self.assertEqual(sum([bin_.get_size() for bin_ in output_]), side*side*side)


class TestOverlappingBinCleaner(unittest.TestCase):
    @perf
    def test_overlapping_bin_cleaner(self):
        bin_list = [Bin(Point3D(x=0, y=0, z=0), 1, 2, 2),
                    Bin(Point3D(x=0, y=0, z=1), 1, 2, 1),
                    Bin(Point3D(x=0, y=0, z=1), 1, 22, 24),
                    Bin(Point3D(x=0, y=0, z=0), 1, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 24, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 24, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 24, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 24, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 1, 24, 24)
                    ]

        self.assertEqual(BinFinder.overlapping_bin_cleaner(bin_list), [Bin(Point3D(x=0, y=0, z=0), 24, 24, 24)])

    def test_overlapping_bin_cleaner_1(self):
        bin_list = [Bin(Point3D(x=0, y=0, z=0), 1, 2, 2),
                    Bin(Point3D(x=0, y=0, z=1), 1, 2, 1),
                    Bin(Point3D(x=0, y=0, z=1), 1, 22, 24),
                    Bin(Point3D(x=0, y=0, z=0), 1, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 1, 24, 24),
                    Bin(Point3D(x=0, y=0, z=0), 1, 24, 24)
                    ]

        self.assertEqual(BinFinder.overlapping_bin_cleaner(bin_list), [Bin(Point3D(x=0, y=0, z=0), 1, 24, 24)])


class TestBinsCollide(unittest.TestCase):
    def test_bins_collide(self):
        bin1 = Bin(Point3D(x=0, y=0, z=0), 1, 2, 2)
        bin2 = Bin(Point3D(x=0, y=0, z=1), 1, 2, 1)

        self.assertTrue(BinFinder.bins_collide(bin1, bin2))

    def test_bins_collide_2(self):
        bin1 = Bin(Point3D(x=0, y=0, z=0), 1, 24, 24)
        bin2 = Bin(Point3D(x=0, y=0, z=1), 1, 22, 24)

        self.assertTrue(BinFinder.bins_collide(bin2, bin1))

    def test_bins_collide_3(self):
        bin1 = Bin(Point3D(x=0, y=0, z=0), 24, 24, 1)
        bin2 = Bin(Point3D(x=0, y=0, z=1), 24, 24, 1)

        self.assertFalse(BinFinder.bins_collide(bin1, bin2))

    def test_bins_collide_4(self):
        bin1 = Bin(Point3D(x=0, y=0, z=1), 1, 2, 1)
        bin2 = Bin(Point3D(x=0, y=0, z=0), 1, 24, 24)

        self.assertTrue(BinFinder.bins_collide(bin1, bin2))

    def test_bins_collide_5(self):
        bin1 = Bin(Point3D(x=0, y=0, z=1), 1, 2, 1)
        bin2 = Bin(Point3D(x=0, y=0, z=0), 1, 24, 24)

        self.assertTrue(BinFinder.bins_collide(bin2, bin1))

if __name__ == '__main__':
    unittest.main()

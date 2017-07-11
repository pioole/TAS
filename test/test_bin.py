import unittest

from src.Bin import Bin
from src.Cluster import Cluster
from src.Exceptions import BinTooSmallException
from src.Job import Job
from src.Timer import Timer
from src.geometry_utils import Point3D


class TestBin(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()
        self.bin_ = Bin(Point3D(0, 0, 0), 4, 1, 1)
        self.cluster = Cluster(Point3D(4, 1, 1), plotting=False, timer=self.timer)
        self.bin_1 = Bin(Point3D(0, 0, 0), 4, 4, 1)
        self.cluster1 = Cluster(Point3D(4, 4, 1), plotting=False, timer=self.timer)
        self.bin_2 = Bin(Point3D(0, 0, 0), 4, 4, 4)
        self.cluster2 = Cluster(Point3D(4, 4, 4), plotting=False, timer=self.timer)
        self.bin_3 = Bin(Point3D(0, 0, 0), 2, 2, 2)
        self.cluster3 = Cluster(Point3D(2, 2, 2), plotting=False, timer=self.timer)
        self.bin_4 = Bin(Point3D(0, 0, 0), 23, 17, 21)
        self.cluster4 = Cluster(Point3D(23, 17, 21), plotting=False, timer=self.timer)
        self.bin_5 = Bin(Point3D(0, 0, 0), 1, 4, 1)
        self.cluster5 = Cluster(Point3D(1, 4, 1), plotting=False, timer=self.timer)
        self.bin_6 = Bin(Point3D(0, 0, 0), 1, 1, 4)
        self.cluster6 = Cluster(Point3D(1, 1, 4), plotting=False, timer=self.timer)

    def test_get_filling_strategy(self):
        strategy1 = self.bin_._get_filling_strategy(Job(None, None, None, 0, None, None))
        strategy2 = self.bin_._get_filling_strategy(Job(None, None, None, 1, None, None))
        self.assertEqual(strategy1.__func__, Bin._cuboid_strategy.__func__)
        self.assertEqual(strategy2.__func__, Bin._zig_zag_strategy.__func__)

    def test_bin_too_small(self):
        job1 = Job(1, 1, 15, 1, self.timer, self.cluster)
        strategy = self.bin_._get_filling_strategy(job1)
        self.assertRaises(BinTooSmallException, strategy, job1, self.cluster, False)

    def test_zigzag(self):
        job2 = Job(1, 1, 4, 1, self.timer, self.cluster)
        strategy = self.bin_._get_filling_strategy(job2)
        strategy(job2, self.cluster, False)

    def test_zigzag_2(self):
        job1 = Job(1, 1, 2, 1, self.timer, self.cluster)
        job2 = Job(1, 1, 2, 1, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)

    def test_zigzag_3(self):
        job1 = Job(1, 1, 7, 1, self.timer, self.cluster1)
        job2 = Job(1, 1, 9, 1, self.timer, self.cluster1)
        strategy1 = self.bin_1._get_filling_strategy(job1)
        strategy2 = self.bin_1._get_filling_strategy(job2)
        strategy1(job1, self.cluster1, False)
        strategy2(job2, self.cluster1, False)

    def test_zigzag_4(self):
        job1 = Job(1, 1, 7, 1, self.timer, self.cluster1)
        job2 = Job(1, 1, 9, 1, self.timer, self.cluster1)
        job3 = Job(1, 1, 1, 1, self.timer, self.cluster1)
        strategy1 = self.bin_1._get_filling_strategy(job1)
        strategy2 = self.bin_1._get_filling_strategy(job2)
        strategy3 = self.bin_1._get_filling_strategy(job3)
        strategy1(job1, self.cluster1, False)
        strategy2(job2, self.cluster1, False)
        self.assertRaises(BinTooSmallException, strategy3, job3, self.cluster1, False)

    def test_cuboid(self):
        job3 = Job(1, 1, 4, 0, self.timer, self.cluster)
        strategy = self.bin_._get_filling_strategy(job3)
        strategy(job3, self.cluster, False)

    def test_cuboid_2(self):
        job1 = Job(1, 1, 2, 0, self.timer, self.cluster)
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)

    def test_cuboid_3(self):
        job1 = Job(1, 1, 7, 0, self.timer, self.cluster1)  # takes two layers
        job2 = Job(1, 1, 8, 0, self.timer, self.cluster1)
        strategy1 = self.bin_1._get_filling_strategy(job1)
        strategy2 = self.bin_1._get_filling_strategy(job2)
        strategy1(job1, self.cluster1, False)
        strategy2(job2, self.cluster1, False)

    def test_cuboid_4(self):
        job1 = Job(1, 1, 1, 0, self.timer, self.cluster)  # takes two layers
        job2 = Job(1, 1, 1, 0, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)

        job1 = Job(1, 1, 1, 0, self.timer, self.cluster5)  # takes two layers
        job2 = Job(1, 1, 1, 0, self.timer, self.cluster5)
        strategy1 = self.bin_5._get_filling_strategy(job1)
        strategy2 = self.bin_5._get_filling_strategy(job2)
        strategy1(job1, self.cluster5, False)
        strategy2(job2, self.cluster5, False)

        job1 = Job(1, 1, 1, 0, self.timer, self.cluster6)  # takes two layers
        job2 = Job(1, 1, 1, 0, self.timer, self.cluster6)
        strategy1 = self.bin_6._get_filling_strategy(job1)
        strategy2 = self.bin_6._get_filling_strategy(job2)
        strategy1(job1, self.cluster6, False)
        strategy2(job2, self.cluster6, False)

    def test_cuboid_5(self):
        job1 = Job(1, 1, 3, 0, self.timer, self.cluster)  # takes two layers
        job2 = Job(1, 1, 1, 0, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)

        job1 = Job(1, 1, 3, 0, self.timer, self.cluster5)  # takes two layers
        job2 = Job(1, 1, 1, 0, self.timer, self.cluster5)
        strategy1 = self.bin_5._get_filling_strategy(job1)
        strategy2 = self.bin_5._get_filling_strategy(job2)
        strategy1(job1, self.cluster5, False)
        strategy2(job2, self.cluster5, False)

        job1 = Job(1, 1, 3, 0, self.timer, self.cluster6)  # takes two layers
        job2 = Job(1, 1, 1, 0, self.timer, self.cluster6)
        strategy1 = self.bin_6._get_filling_strategy(job1)
        strategy2 = self.bin_6._get_filling_strategy(job2)
        strategy1(job1, self.cluster6, False)
        strategy2(job2, self.cluster6, False)

    def test_cuboid_6(self):
        job1 = Job(1, 1, 1, 0, self.timer, self.cluster)  # takes two layers
        job2 = Job(1, 1, 3, 0, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)

        job1 = Job(1, 1, 1, 0, self.timer, self.cluster5)  # takes two layers
        job2 = Job(1, 1, 3, 0, self.timer, self.cluster5)
        strategy1 = self.bin_5._get_filling_strategy(job1)
        strategy2 = self.bin_5._get_filling_strategy(job2)
        strategy1(job1, self.cluster5, False)
        strategy2(job2, self.cluster5, False)

        job1 = Job(1, 1, 1, 0, self.timer, self.cluster6)  # takes two layers
        job2 = Job(1, 1, 3, 0, self.timer, self.cluster6)
        strategy1 = self.bin_6._get_filling_strategy(job1)
        strategy2 = self.bin_6._get_filling_strategy(job2)
        strategy1(job1, self.cluster6, False)
        strategy2(job2, self.cluster6, False)

    def test_cuboid_7(self):
        job1 = Job(1, 1, 2, 0, self.timer, self.cluster)  # takes two layers
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)

        job1 = Job(1, 1, 2, 0, self.timer, self.cluster5)  # takes two layers
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster5)
        strategy1 = self.bin_5._get_filling_strategy(job1)
        strategy2 = self.bin_5._get_filling_strategy(job2)
        strategy1(job1, self.cluster5, False)
        strategy2(job2, self.cluster5, False)

        job1 = Job(1, 1, 2, 0, self.timer, self.cluster6)  # takes two layers
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster6)
        strategy1 = self.bin_6._get_filling_strategy(job1)
        strategy2 = self.bin_6._get_filling_strategy(job2)
        strategy1(job1, self.cluster6, False)
        strategy2(job2, self.cluster6, False)

    def test_cuboid_8(self):
        job1 = Job(1, 1, 1, 0, self.timer, self.cluster)  # takes two layers
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster)
        job3 = Job(1, 1, 1, 0, self.timer, self.cluster)
        strategy1 = self.bin_._get_filling_strategy(job1)
        strategy2 = self.bin_._get_filling_strategy(job2)
        strategy3 = self.bin_._get_filling_strategy(job3)
        strategy1(job1, self.cluster, False)
        strategy2(job2, self.cluster, False)
        strategy3(job3, self.cluster, False)

        job1 = Job(1, 1, 1, 0, self.timer, self.cluster5)  # takes two layers
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster5)
        job3 = Job(1, 1, 1, 0, self.timer, self.cluster5)
        strategy1 = self.bin_5._get_filling_strategy(job1)
        strategy2 = self.bin_5._get_filling_strategy(job2)
        strategy3 = self.bin_5._get_filling_strategy(job3)
        strategy1(job1, self.cluster5, False)
        strategy2(job2, self.cluster5, False)
        strategy3(job3, self.cluster5, False)

        job1 = Job(1, 1, 1, 0, self.timer, self.cluster6)  # takes two layers
        job2 = Job(1, 1, 2, 0, self.timer, self.cluster6)
        job3 = Job(1, 1, 1, 0, self.timer, self.cluster6)
        strategy1 = self.bin_6._get_filling_strategy(job1)
        strategy2 = self.bin_6._get_filling_strategy(job2)
        strategy3 = self.bin_6._get_filling_strategy(job3)
        strategy1(job1, self.cluster6, False)
        strategy2(job2, self.cluster6, False)
        strategy3(job3, self.cluster6, False)

    def test_mixed(self):
        job1 = Job(1, 1, 7, 1, self.timer, self.cluster1)
        job2 = Job(1, 1, 1, 1, self.timer, self.cluster1)
        job3 = Job(1, 1, 8, 0, self.timer, self.cluster1)
        strategy1 = self.bin_1._get_filling_strategy(job1)
        strategy2 = self.bin_1._get_filling_strategy(job2)
        strategy3 = self.bin_1._get_filling_strategy(job3)
        strategy1(job1, self.cluster1, False)
        strategy2(job2, self.cluster1, False)
        strategy3(job3, self.cluster1, False)

    def test_mixed_1(self):
        job1 = Job(1, 1, 31, 1, self.timer, self.cluster2)
        job2 = Job(1, 1, 1, 1, self.timer, self.cluster2)
        job3 = Job(1, 1, 28, 0, self.timer, self.cluster2)
        strategy1 = self.bin_2._get_filling_strategy(job1)
        strategy2 = self.bin_2._get_filling_strategy(job2)
        strategy3 = self.bin_2._get_filling_strategy(job3)
        strategy1(job1, self.cluster2, False)
        strategy2(job2, self.cluster2, False)
        strategy3(job3, self.cluster2, False)

    def test_mixed_2(self):
        job1 = Job(1, 1, 31, 1, self.timer, self.cluster2)
        job2 = Job(1, 1, 2, 1, self.timer, self.cluster2)
        job3 = Job(1, 1, 28, 0, self.timer, self.cluster2)
        strategy1 = self.bin_2._get_filling_strategy(job1)
        strategy2 = self.bin_2._get_filling_strategy(job2)
        strategy3 = self.bin_2._get_filling_strategy(job3)
        strategy1(job1, self.cluster2, False)
        strategy2(job2, self.cluster2, False)
        self.assertRaises(BinTooSmallException, strategy3, job3, self.cluster2, False)

    def test_mixed_3(self):
        job2 = Job(2, 1, 1, 1, self.timer, self.cluster2)
        job4 = Job(4, 1, 12, 1, self.timer, self.cluster2)
        strategy2 = self.bin_2._get_filling_strategy(job2)
        strategy4 = self.bin_2._get_filling_strategy(job4)
        strategy2(job2, self.cluster2, False)
        strategy4(job4, self.cluster2, False)

    def test_mixed_4(self):
        job1 = Job(1, 1, 3, 1, self.timer, self.cluster3)
        job2 = Job(2, 1, 1, 1, self.timer, self.cluster3)
        job3 = Job(3, 1, 5, 0, self.timer, self.cluster3)
        strategy1 = self.bin_3._get_filling_strategy(job1)
        strategy2 = self.bin_3._get_filling_strategy(job2)
        strategy3 = self.bin_3._get_filling_strategy(job3)
        strategy1(job1, self.cluster3, False)
        strategy2(job2, self.cluster3, False)
        self.assertRaises(BinTooSmallException, strategy3, job3, self.cluster3, False)

    def test_mixed_5(self):
        job1 = Job(1, 1, 1, 1, self.timer, self.cluster3)
        job2 = Job(2, 1, 3, 1, self.timer, self.cluster3)
        strategy1 = self.bin_3._get_filling_strategy(job1)
        strategy2 = self.bin_3._get_filling_strategy(job2)
        strategy1(job1, self.cluster3, False)
        strategy2(job2, self.cluster3, False)

    def test_mixed_6(self):
        job_list = [
            Job(1, 1, 1, 1, self.timer, self.cluster3),
            Job(2, 1, 2, 0, self.timer, self.cluster3),
            Job(3, 1, 1, 1, self.timer, self.cluster3),
            Job(4, 1, 2, 0, self.timer, self.cluster3),
            Job(4, 1, 2, 1, self.timer, self.cluster3),
        ]
        for job in job_list:
            strategy = self.bin_3._get_filling_strategy(job)
            strategy(job, self.cluster3, False)

    def test_mixed_7(self):
        job_list = [
            Job(4, 1, 2, 0, self.timer, self.cluster3),
            Job(1, 1, 1, 1, self.timer, self.cluster3),
            Job(3, 1, 1, 1, self.timer, self.cluster3),
            Job(2, 1, 1, 0, self.timer, self.cluster3),
            Job(4, 1, 2, 1, self.timer, self.cluster3),
        ]
        for job in job_list:
            strategy = self.bin_3._get_filling_strategy(job)
            strategy(job, self.cluster3, False)

    def test_mixed_8(self):
        job_list = [
            Job(4, 1, 9, 1, self.timer, self.cluster2),
            Job(4, 1, 3, 1, self.timer, self.cluster2),
            Job(4, 1, 7, 0, self.timer, self.cluster2),
            Job(4, 1, 3, 0, self.timer, self.cluster2),
            Job(4, 1, 2, 1, self.timer, self.cluster2),
            Job(4, 1, 1, 1, self.timer, self.cluster2),
        ]
        for job in job_list:
            strategy = self.bin_2._get_filling_strategy(job)
            strategy(job, self.cluster2, False)

    def test_mixed_9(self):
        job_list = [
            Job(1, 1, 4, 1, self.timer, self.cluster2),
            Job(2, 1, 17, 0, self.timer, self.cluster2),
            Job(3, 1, 5, 0, self.timer, self.cluster2),
        ]
        job1 = Job(4, 1, 9, 0, self.timer, self.cluster2)
        for job in job_list:
            strategy = self.bin_2._get_filling_strategy(job)
            strategy(job, self.cluster2, False)
        strategy = self.bin_2._get_filling_strategy(job1)
        self.assertRaises(BinTooSmallException, strategy, job1, self.cluster2, False)

    def test_mixed_10(self):
        job_list = [
            Job(1, 1, 4, 1, self.timer, self.cluster2),
            Job(2, 1, 2, 0, self.timer, self.cluster2),
            Job(2, 1, 2, 0, self.timer, self.cluster2),
            Job(2, 1, 2, 0, self.timer, self.cluster2),
            Job(2, 1, 2, 1, self.timer, self.cluster2),
            Job(2, 1, 9, 1, self.timer, self.cluster2),
            Job(2, 1, 7, 1, self.timer, self.cluster2),
            Job(2, 1, 11, 1, self.timer, self.cluster2),
            Job(3, 1, 15, 1, self.timer, self.cluster2),
        ]
        for job in job_list:
            strategy = self.bin_2._get_filling_strategy(job)
            strategy(job, self.cluster2, False)

    def test_mixed_11(self):
        job1 = Job(1, 1, 8210, 0, self.timer, self.cluster4)
        job2 = Job(2, 1, 1, 1, self.timer, self.cluster4)
        strategy1 = self.bin_4._get_filling_strategy(job1)
        strategy2 = self.bin_4._get_filling_strategy(job2)
        strategy1(job1, self.cluster4, False)
        self.assertRaises(BinTooSmallException, strategy2, job2, self.cluster4, False)

    def test_mixed_12(self):
        job_list = [
            Job(1, 1, 8, 0, self.timer, self.cluster3),
        ]
        job1 = Job(2, 1, 1, 1, self.timer, self.cluster3)
        for job in job_list:
            strategy = self.bin_3._get_filling_strategy(job)
            strategy(job, self.cluster3, False)
        strategy = self.bin_3._get_filling_strategy(job1)
        self.assertRaises(BinTooSmallException, strategy, job1, self.cluster3, False)

if __name__ == '__main__':
    unittest.main()

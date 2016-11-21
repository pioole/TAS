import unittest

from src.Cluster import Cluster
from src.Job import Job
from src.Timer import Timer
from src.geometry_utils import Point3D


class TestJob(unittest.TestCase):
    def setUp(self):
        self.timer = Timer(13)
        self.cluster = Cluster(Point3D(24, 24, 24))

    def test_job_1(self):
        job = Job(1, 12, 32, 1, self.timer, self.cluster)
        self.assertEqual(job.job_id, 1)
        self.assertEqual(job.comm_sensitive, 1)
        self.assertEqual(job.nodes_needed, 32)
        self.assertEqual(job.work_time, 12)

    def test_job_2(self):
        job = Job(1, 12, 32, 1, self.timer, self.cluster)
        self.assertFalse(job.completed())

    def test_job_3(self):
        job = Job(1, 12, 32, 1, self.timer, self.cluster)
        job.start_job()
        self.assertFalse(job.completed())

    def test_job_4(self):
        job = Job(1, 12, 32, 1, self.timer, self.cluster)
        job.start_job()
        self.timer.tick()
        self.assertTrue(job.completed())



import unittest

from src.Cluster import Cluster
from src.JobGenerator import JobGenerator
from src.Job import Job
from src.Timer import Timer
from src.geometry_utils import Point3D


class TestJobGenerator(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()
        self.cluster = Cluster(Point3D(24, 24, 24), plotting=False, timer=self.timer)

    def test_job_generator_1(self):
        generator = JobGenerator(self.timer, self.cluster)
        batch = generator.draw_jobs(112)
        self.assertEqual(len(batch), 112)

    def test_job_generator_2(self):
        generator = JobGenerator(self.timer, self.cluster)
        batch = generator.draw_jobs(3)
        self.assertTrue(type(batch[1]) == Job)

    def test_job_generator_3(self):
        generator = JobGenerator(self.timer, self.cluster)
        batch = generator.draw_jobs(5112)
        self.assertEqual(len(batch), 5112)

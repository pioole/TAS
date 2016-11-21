import unittest

from src.Cluster import Cluster
from src.JobGenerator import JobGenerator
from src.JobQueue import JobQueue
from src.Timer import Timer
from src.geometry_utils import Point3D


class TestUpdateJobQueue(unittest.TestCase):
    def test_update_job_queue_1(self):
        cluster = Cluster(Point3D(4, 4, 4))
        timer = Timer()
        job_generator = JobGenerator(timer, cluster)
        job_list = job_generator.draw_jobs(8)
        job_queue = JobQueue()

        job_queue.fill_queue_with_jobs(job_list)

        cluster.update_job_queue(job_list, plot=False)

        self.assertEqual(job_queue, cluster.job_queue)
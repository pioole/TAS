import unittest

from src.Cluster import Cluster
from src.Job import Job
from src.Timer import Timer
from src.geometry_utils import Point3D


class TestBackfilling(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()
        self.cluster = Cluster(Point3D(2, 1, 1), plotting=False, timer=self.timer, backfill_depth=1)

    def test_backfilling(self):
        job_1 = Job(1, 45, 1, 1, self.timer, self.cluster)
        b_job = Job(2, 15, 2, 1, self.timer, self.cluster)
        job_3 = Job(3, 15, 1, 1, self.timer, self.cluster)
        job_4 = Job(4, 15, 1, 1, self.timer, self.cluster)
        job_5 = Job(5, 15, 1, 1, self.timer, self.cluster)

        job_list = [
            job_1,
            b_job,
            job_3,
            job_4,
            job_5,
            Job(6, 1, 1, 1, self.timer, self.cluster),
            Job(7, 1, 1, 1, self.timer, self.cluster),
            Job(8, 1, 1, 1, self.timer, self.cluster),
            Job(9, 1, 1, 1, self.timer, self.cluster),
            Job(10, 1, 1, 1, self.timer, self.cluster),
        ]
        self.cluster.update_job_queue(job_list)

        self.cluster.run_time_tick()  # 0 - 15
        self.assertTrue(b_job in self.cluster.backfill_jobs)
        self.assertTrue(b_job not in self.cluster.running_jobs)
        self.assertTrue(job_1 in self.cluster.running_jobs)
        self.assertTrue(job_3 in self.cluster.running_jobs)
        self.assertTrue(job_4 not in self.cluster.running_jobs)
        self.assertTrue(job_5 not in self.cluster.running_jobs)

        self.cluster.run_time_tick()  # 15 - 30

        self.assertTrue(b_job in self.cluster.backfill_jobs)
        self.assertTrue(b_job not in self.cluster.running_jobs)
        self.assertTrue(job_1 in self.cluster.running_jobs)
        self.assertTrue(job_3 not in self.cluster.running_jobs)
        self.assertTrue(job_4 in self.cluster.running_jobs)
        self.assertTrue(job_5 not in self.cluster.running_jobs)

        self.cluster.run_time_tick()  # 30 - 45

        self.assertTrue(b_job in self.cluster.backfill_jobs)
        self.assertTrue(b_job not in self.cluster.running_jobs)
        self.assertTrue(job_1 in self.cluster.running_jobs)
        self.assertTrue(job_4 not in self.cluster.running_jobs)
        self.assertTrue(job_5 in self.cluster.running_jobs)

        self.cluster.run_time_tick()  # 45 - 60

        self.assertTrue(b_job not in self.cluster.backfill_jobs)
        self.assertTrue(b_job in self.cluster.running_jobs)
        self.assertTrue(job_1 not in self.cluster.running_jobs)
        self.assertTrue(job_5 not in self.cluster.running_jobs)

        self.cluster.run_time_tick()  # 60 - 75

        self.assertTrue(b_job not in self.cluster.running_jobs)


if __name__ == '__main__':
    unittest.main()

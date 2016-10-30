import unittest

from src.Job import Job


class TestJob(unittest.TestCase):
    def test_job_1(self):
        job = Job(1, 12, 32, 1)
        self.assertEqual(job.job_id, 1)
        self.assertEqual(job.comm_sensitive, 1)
        self.assertEqual(job.nodes_needed, 32)
        self.assertEqual(job.work_time, 12)

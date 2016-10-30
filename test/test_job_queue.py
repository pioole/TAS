import unittest

from src.JobQueue import JobQueue
from src.Job import Job


class TestJobQueue(unittest.TestCase):
    def setUp(self):
        self.queue = JobQueue()
        self.job1 = Job(1, 12, 32, 1)
        self.job2 = Job(2, 12, 32, 1)
        self.job3 = Job(3, 12, 32, 1)
        self.job4 = Job(4, 12, 32, 1)
        self.queue.fill_queue_with_jobs([self.job1, self.job2, self.job3, self.job4])

    def test_job_queue_1(self):
        self.assertEqual(len(self.queue), 4)

    def test_job_queue_2(self):
        self.assertEqual(self.queue.peek_at_first_job(), self.job1)

    def test_job_queue_3(self):
        self.assertEqual(self.queue.pop_first(), self.job1)
        self.assertEqual(len(self.queue), 3)

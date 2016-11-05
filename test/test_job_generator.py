import unittest

from src.JobGenerator import JobGenerator
from src.Job import Job
from src.Timer import Timer


class TestJobGenerator(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()

    def test_job_generator_1(self):
        generator = JobGenerator(self.timer)
        batch = generator.draw_jobs(112)
        self.assertEqual(len(batch), 112)

    def test_job_generator_2(self):
        generator = JobGenerator(self.timer)
        batch = generator.draw_jobs(3)
        self.assertTrue(type(batch[1]) == Job)

    def test_job_generator_3(self):
        generator = JobGenerator(self.timer)
        batch = generator.draw_jobs(5112)
        self.assertEqual(len(batch), 5112)

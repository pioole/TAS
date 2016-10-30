from collections import namedtuple
from random import shuffle, randint

from src.Job import Job

JobNodeCharacteristics = namedtuple('JobNodeCharacteristics', 'amount bottom_no_of_nodes top_no_of_jobs')
JobTimeCharacteristics = namedtuple('JobTimeCharacteristics', 'minimal_time maximal_time amount')
JobNodeData = namedtuple('JobNodeData', 'no_of_nodes')
JobTimeData = namedtuple('JobTimeData', 'time_needed')

job_node_data = [
    JobNodeCharacteristics(3679, 1, 1),  # create 3679 jobs using 1 node.
    JobNodeCharacteristics(876, 2, 9),  # TODO: remove magic numbers
    JobNodeCharacteristics(273, 10, 50),
    JobNodeCharacteristics(172, 50, 101)
]

job_time_data = [
    JobTimeCharacteristics(1, 61, 2407),
    JobTimeCharacteristics(61, 121, 465),
    JobTimeCharacteristics(121, 181, 93),
    JobTimeCharacteristics(181, 241, 84),
    JobTimeCharacteristics(241, 301, 190),
    JobTimeCharacteristics(301, 361, 123),
    JobTimeCharacteristics(361, 421, 75),
    JobTimeCharacteristics(421, 481, 61),
    JobTimeCharacteristics(481, 541, 90),
    JobTimeCharacteristics(541, 601, 93),
    JobTimeCharacteristics(601, 661, 68),
    JobTimeCharacteristics(661, 721, 50),
    JobTimeCharacteristics(721, 781, 47),
    JobTimeCharacteristics(781, 841, 33),
    JobTimeCharacteristics(841, 901, 50),
    JobTimeCharacteristics(901, 961, 37),
    JobTimeCharacteristics(961, 1021, 68),
    JobTimeCharacteristics(1021, 1081, 106),
    JobTimeCharacteristics(1081, 1141, 131),
    JobTimeCharacteristics(1141, 1201, 107),
    JobTimeCharacteristics(1201, 1261, 85),
    JobTimeCharacteristics(1261, 1321, 109),
    JobTimeCharacteristics(1321, 1381, 104),
    JobTimeCharacteristics(1381, 1441, 324)
]


class JobGenerator(object):
    def __init__(self, buffer_size=5000):
        """
        initiates a JobGenerator object with given buffer size.
        :param buffer_size: Int
        :return: JobGenerator
        """
        self.available_jobs = []
        self.generate_job_batch()

    def generate_job_batch(self):
        """
        Creates a new batch of jobs according to the given distribution (top of this file) and appends it to the job list.

        For now we only create communication sensitive jobs. #TODO

        :return: None
        """
        node_data = [
            [
                JobNodeData(
                        randint(node_characteristic.bottom_no_of_nodes,
                                node_characteristic.top_no_of_jobs))
                for _ in xrange(node_characteristic.amount)
                ]
            for node_characteristic in job_node_data
            ]

        time_data = [
            [
                JobTimeData(
                        randint(node_characteristic.minimal_time,
                                node_characteristic.maximal_time))
                for _ in xrange(node_characteristic.amount)
                ]
            for node_characteristic in job_time_data
            ]

        time_data = sum(time_data, [])
        node_data = sum(node_data, [])

        assert len(time_data) == len(node_data)  # just in case, as we are using magick numbers..

        shuffle(node_data)
        shuffle(time_data)

        job_batch = [Job(job_id, time.time_needed, node.no_of_nodes, 0) for time, node, job_id in
                     zip(time_data, node_data, xrange(1, 1 + len(time_data)))]

        self.available_jobs.extend(job_batch)

    def draw_jobs(self, no_of_jobs):
        """
        Returns (and generates if needed) the requested amount of jobs.
        :param no_of_jobs: Int
        :return: [Job]
        """
        while no_of_jobs > len(self.available_jobs):
            self.generate_job_batch()
        list_to_draw = self.available_jobs[:no_of_jobs]
        self.available_jobs = self.available_jobs[no_of_jobs + 1:]
        return list_to_draw

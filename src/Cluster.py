import numpy as np

from MaxRecSize import max_size
from operator import mul
from JobQueue import JobQueue
from plotting import Plotter
from plotting3D import Plotter3D
from src.Exceptions import NoBinsAvailableException, BinTooSmallException
from src.JobGenerator import JobGenerator


class Cluster(object):
    def __init__(self, cluster_size):
        """
        initiates the computing cluster simulation object
        :param cluster_size: Point3D
        :return: Cluster
        """
        self.cluster_size = cluster_size
        self.job_queue = JobQueue()
        self.available_bins = []
        self.node_matrix = np.zeros((self.cluster_size.x, self.cluster_size.y, self.cluster_size.z))
        self.queue_size_plotter = Plotter()
        self.plotter3D = Plotter3D()
        self.running_jobs = []

    def update_job_queue(self, job_list):
        """
        fills clusters job queue with new list of given jobs.
        :param job_list: [Job]
        :return: None
        """
        self.job_queue.fill_queue_with_jobs(job_list)
        self.queue_size_plotter.plot(len(self.job_queue))

    def _update_available_bins_list(self):
        self.available_bins = []

    def _mark_bin_as_used(self, bin_):
        """
        removes the given Bin object from the 'available bins' list as it is already filled in.
        :param bin_: Bin
        :return: None
        """
        self.available_bins.remove(bin_)

    def _get_biggest_available_bin(self):
        """
        returns biggest bin available for filling in, or raises NoBinsAvailableException if there are no available bins.
        :return: Bin
        """
        try:
            return self.available_bins[0]
        except IndexError:
            raise NoBinsAvailableException()

    def _fill_available_bins(self):
        filling_in = True
        while filling_in:
            try:
                bin_ = self._get_biggest_available_bin()
                bin_.fill_in(self.job_queue)
                self._mark_bin_as_used(bin_)
            except (NoBinsAvailableException, BinTooSmallException):
                filling_in = False

    def _remove_finished_jobs(self):
        # for job in self.running_jobs:
        #     if job.completed():
        pass

    def work_to_do(self):
        """
        indicates whether there are still jobs waiting in queue
        :return: bool
        """
        return bool(self.job_queue.job_list)

    def run_time_tick(self):
        """
        runs one iteration of the packing algorithm. The iteration stops if there is no more space in cluster or if
        the job queue is empty.
        :return:
        """
        self._remove_finished_jobs()
        self._update_available_bins_list()
        self._fill_available_bins()
        self.queue_size_plotter.plot(len(self.job_queue))


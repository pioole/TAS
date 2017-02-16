import numpy as np
import logging

from JobQueue import JobQueue
from plotting import Plotter
from plotting3D import Plotter3D
from src.BinFinder import BinFinder
from src.Exceptions import NoBinsAvailableException, BinTooSmallException, UnAuthorisedAccessException
from performance import perf


class Cluster(object):
    def __init__(self, cluster_size, plotting=False):
        """
        initiates the computing cluster simulation object
        :param cluster_size: Point3D
        :return: Cluster
        """
        self.cluster_size = cluster_size
        self.job_queue = JobQueue()
        self.available_bins = []
        self._node_matrix = np.zeros((self.cluster_size.x, self.cluster_size.y, self.cluster_size.z))
        if plotting:
            self.queue_size_plotter = Plotter()
            self.plotter3D = Plotter3D()
        self.running_jobs = []
        self.bin_finder = BinFinder(self.cluster_size.x)

    @perf
    def update_job_queue(self, job_list, plot=True):
        """
        fills clusters job queue with new list of given jobs.
        Shows the job_size plot when 'plot' is set to True
        :param job_list: [Job]
        :param plot: Bool
        :return: None
        """
        self.job_queue.fill_queue_with_jobs(job_list)
        if plot:
            self.queue_size_plotter.plot(len(self.job_queue))

    @perf
    def _update_available_bins_list(self):
        """
        Finds all available bins and puts them into available_bins list.
        :return: None
        """
        self.available_bins = self.bin_finder.get_available_bins(self._node_matrix)

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
            return max(self.available_bins, key=lambda bin_: bin_.get_size())
        except ValueError:
            raise NoBinsAvailableException()

    @perf
    def _fill_available_bins(self):
        filling_in = True
        while filling_in:
            try:
                bin_ = self._get_biggest_available_bin()
                bin_.fill_in(self.job_queue, self)
                self._mark_bin_as_used(bin_)
            except (NoBinsAvailableException, BinTooSmallException):
                filling_in = False

    @perf
    def _remove_finished_jobs(self):
        """
        removes completed job from the cluster, and running_jobs list
        returns number of removed jobs
        :return: Int
        """
        to_remove = []
        for job in self.running_jobs:
            if job.completed():
                job.free_nodes()
                to_remove.append(job)
        no_of_jobs_removed = len(to_remove)
        self.running_jobs = list(set(self.running_jobs) - set(to_remove))
        return no_of_jobs_removed

    def assign_nodes(self, job_id, node_list, job):
        """
        Assigns nodes from the list to the given job_id, and adds a job to the running jobs list.
        :param job_id: Int
        :param node_list: [Point3D]
        :return:
        """
        for node in node_list:
            if self._node_matrix[node.x][node.y][node.z] == 0:
                self._node_matrix[node.x][node.y][node.z] = job_id
            else:
                logging.error('job {} tried to overwrite job {} at {} {} {}'.format(job_id,
                                                                                    self._node_matrix[node.x][node.y][node.z],
                                                                                    node.x,
                                                                                    node.y,
                                                                                    node.z))
                raise UnAuthorisedAccessException()
        self.running_jobs.append(job)
        job.start_job()

    def free_nodes(self, job_id, node_list):
        """
        removes the job from given nodes
        :param job_id: Int
        :param node_list: [Point3D]
        :return: None
        """
        for node in node_list:
            if self._node_matrix[node.x][node.y][node.z] == job_id:
                self._node_matrix[node.x][node.y][node.z] = 0
            else:
                raise UnAuthorisedAccessException()

    def work_to_do(self):
        """
        indicates whether there are still jobs waiting in queue
        :return: bool
        """
        return bool(self.job_queue.job_list)

    def plot_3D(self):
        plot_points = []
        for job in self.running_jobs:
            xs = []
            ys = []
            zs = []
            for node in job.node_list:
                xs.append(node.x)
                ys.append(node.y)
                zs.append(node.z)
            plot_points.append((xs, ys, zs, len(plot_points)))

        self.plotter3D.plot(plot_points)

    def run_time_tick(self):
        """
        runs one iteration of the packing algorithm. The iteration stops if there is no more space in cluster or if
        the job queue is empty.
        :return:
        """
        logging.info('### New Time Tick #########################')
        no_of_jobs_removed = self._remove_finished_jobs()
        logging.info('{} jobs removed after last iteration'.format(no_of_jobs_removed))
        self._update_available_bins_list()
        logging.info('{} BIN(S) AVAILABLE'.format(len(self.available_bins)))
        self._fill_available_bins()
        logging.info('{} JOB(S) RUNNING'.format(len(self.running_jobs)))
        self.queue_size_plotter.plot(len(self.job_queue))
        self.plot_3D()


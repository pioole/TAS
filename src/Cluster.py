import numpy as np
import logging
import copy

from JobQueue import JobQueue
from plotting import Plotter
from plotting3D import Plotter3D
from src.BinFinder import BinFinder
from src.Exceptions import NoBinsAvailableException, BinTooSmallException, UnAuthorisedAccessException, \
    BackfillJobPriorityException
from performance import perf


class Cluster(object):
    def __init__(self, cluster_size, timer, plotting=False, minimal_bin_size=1, backfill_depth=0):
        """
        initiates the computing cluster simulation object
        :param cluster_size: Point3D
        :return: Cluster
        """
        self.cluster_size = cluster_size
        self.job_queue = JobQueue()
        self.available_bins = []
        self._node_matrix = np.zeros((self.cluster_size.x, self.cluster_size.y, self.cluster_size.z))
        self.plotting = plotting
        if plotting:
            self.queue_size_plotter = Plotter(1)
            self.plotter3D = Plotter3D(2)
            self.cluster_utilization_plotter = Plotter(3)
        self.running_jobs = []
        self.bin_finder = BinFinder(self.cluster_size.x, minimal_bin_size)
        self.backfill_jobs = []
        self.backfill_depth = backfill_depth
        self.timer = timer

    @perf
    def update_job_queue(self, job_list):
        """
        fills clusters job queue with new list of given jobs.
        Shows the job_size plot when 'plot' is set to True
        :param job_list: [Job]
        :param plot: Bool
        :return: None
        """
        self.job_queue.fill_queue_with_jobs(job_list)
        if self.plotting:
            self.queue_size_plotter.plot(len(self.job_queue))

    @perf
    def _update_available_bins_list(self):
        """
        Finds all available bins and puts them into available_bins list.
        :return: None
        """
        running_nodes = np.count_nonzero(self._node_matrix)
        logging.debug('zero values in matrix: {}'.format(self._node_matrix.size - running_nodes))
        self.available_bins = self.bin_finder.get_available_bins(self._node_matrix)
        logging.debug('bin summary size: {}'.format(sum([bin_.get_size() for bin_ in self.available_bins])))

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
        """
        fills bins from self.available_bins with jobs from self.job_queue
        :return: None
        """
        try:
            first_backfill_job = min(self.backfill_jobs, key=lambda x: x.start_time)
            max_length = first_backfill_job.start_time - self.timer.time()
        except ValueError:
            max_length = -1

        filling_in = True
        while filling_in:
            try:
                bin_ = self._get_biggest_available_bin()
                self._mark_bin_as_used(bin_)
                bin_.check_if_empty(self)
                bin_.fill_in(self.job_queue, self, max_length=max_length)
            except BinTooSmallException:
                pass
            except BackfillJobPriorityException:
                filling_in = False
            except NoBinsAvailableException:
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
        :param job: Job
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
                logging.error('job: {}'.format(job))
                logging.error('sensitive: {}'.format(job.comm_sensitive))
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
        """
        creates a plot of all currently running jobs in order to visualize them
        :return: None
        """
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

    @perf
    def count_cluster_utilization(self):
        """
        returns current fraction of cluster utilization
        :return: Float
        """
        running_nodes = sum([job.nodes_needed for job in self.running_jobs])
        logging.debug('non-zero values in matrix: {}'.format(running_nodes))
        return 1. * running_nodes / self._node_matrix.size

    def insert_backfill_jobs(self):
        for job in self.backfill_jobs:
            if self.timer.time() >= job.start_time:
                job.posess_nodes(job.node_list)
        self.backfill_jobs = filter(lambda job: job.start_time > self.timer.time(), self.backfill_jobs)

    def run_time_tick(self):
        """
        runs one iteration of the packing algorithm. The iteration stops if there is no more space in cluster or if
        the job queue is empty.
        :return:
        """
        logging.debug('### New Time Tick #########################')
        no_of_jobs_removed = self._remove_finished_jobs()
        logging.debug('{} jobs removed after last iteration'.format(no_of_jobs_removed))
        self.insert_backfill_jobs()
        self._update_available_bins_list()
        logging.debug('{} BIN(S) AVAILABLE'.format(len(self.available_bins)))
        self._fill_available_bins()
        logging.debug('{} JOB(S) RUNNING'.format(len(self.running_jobs)))
        cluster_utilization = self.count_cluster_utilization()
        logging.debug('Current cluster utilization: {}'.format(cluster_utilization))
        job_queue_size = len(self.job_queue)
        logging.debug('Current queue size: {}'.format(job_queue_size))

        backfill_rounds = self.backfill_depth
        while backfill_rounds > 0:
            blocking_job = self.job_queue.peek_at_first_job()
            cluster_copy = copy.deepcopy(self)
            cluster_copy.backfill_depth = 0
            intervals = 0

            while blocking_job == cluster_copy.job_queue.peek_at_first_job():
                cluster_copy.run_time_tick()
                intervals += 1
            backfilled_job = cluster_copy.running_jobs[cluster_copy.running_jobs.index(blocking_job)]
            blocking_job = self.job_queue.pop_first()
            blocking_job.node_list = copy.deepcopy(backfilled_job.node_list)
            blocking_job.start_time = backfilled_job.start_time
            self.backfill_jobs.append(blocking_job)

            self._update_available_bins_list()
            logging.debug('{} BIN(S) AVAILABLE'.format(len(self.available_bins)))
            self._fill_available_bins()
            logging.debug('{} JOB(S) RUNNING'.format(len(self.running_jobs)))
            cluster_utilization = self.count_cluster_utilization()
            logging.debug('Current cluster utilization: {}'.format(cluster_utilization))
            job_queue_size = len(self.job_queue)
            logging.debug('Current queue size: {}'.format(job_queue_size))

            backfill_rounds -= 1

        if self.plotting:
            self.cluster_utilization_plotter.plot(cluster_utilization)
            self.queue_size_plotter.plot(job_queue_size)
            self.plot_3D()
        self.timer.tick()


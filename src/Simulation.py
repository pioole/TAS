import logging
import numpy as np

from src.JobGenerator import JobGenerator
from src.Cluster import Cluster
from src.Timer import Timer
from src.geometry_utils import Point3D

CLUSTER_SIDE_LENGTH = 24
LOGGING_LEVEL = logging.DEBUG


def main(minimal_bin_size, comm_sensitivity_percentage):
    ITERATIONS = 30

    logging.basicConfig(level=LOGGING_LEVEL)
    cluster_size = Point3D(CLUSTER_SIDE_LENGTH, CLUSTER_SIDE_LENGTH, CLUSTER_SIDE_LENGTH)

    timer = Timer()
    cluster = Cluster(cluster_size, timer, plotting=False, minimal_bin_size=minimal_bin_size, backfill_depth=3)

    job_generator = JobGenerator(timer, cluster, comm_sensitive_percentage=comm_sensitivity_percentage)

    cluster.update_job_queue(job_generator.draw_jobs(5000))

    utilizations = []

    while cluster.work_to_do() and ITERATIONS > 0:
        cluster.run_time_tick()
        utilizations.append(cluster.count_cluster_utilization())
        logging.info('TIME: {}'.format(timer.time()))
        ITERATIONS -= 1

    logging.info('UTILIZATION_LIST: {} for minimal_bin_size: {} and comm_sensitivity_percentage: {}'.format(utilizations, minimal_bin_size, comm_sensitivity_percentage))
    logging.info('UTILIZATION_MEAN: {} for minimal_bin_size: {} and comm_sensitivity_percentage: {}'.format(np.mean(utilizations), minimal_bin_size, comm_sensitivity_percentage))

    # cluster.queue_size_plotter.preserve_window()

if __name__ == "__main__":
    logging.basicConfig(level=LOGGING_LEVEL)
    for x in xrange(1, 24*24, 10):
        for y in xrange(0, 110, 10):
            pass
    logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\nRUNNING SIMULATION FOR minimal_bin_size={}'
                 ' and comm_sensitivity_percentage: {}'.format(1, 100))
    main(1, 100)

import logging
import numpy as np

from src.JobGenerator import JobGenerator
from src.Cluster import Cluster
from src.Timer import Timer
from src.geometry_utils import Point3D

CLUSTER_SIDE_LENGTH = 24
LOGGING_LEVEL = logging.INFO
CROP = 3000
BACKFILLING_LEVEL = 1
FITTING_STRATEGY = Cluster.FittingStrategy.best_fit
MAX_JOB_SIZE = 500
BUFFER_SIZE = 1100


def main(minimal_bin_size, comm_sensitivity_percentage):
    ITERATIONS = 120

    logging.basicConfig(level=LOGGING_LEVEL)
    cluster_size = Point3D(CLUSTER_SIDE_LENGTH, CLUSTER_SIDE_LENGTH, CLUSTER_SIDE_LENGTH)

    timer = Timer()
    cluster = Cluster(cluster_size, timer,
                      plotting=False,
                      minimal_bin_size=minimal_bin_size,
                      backfill_depth=BACKFILLING_LEVEL,
                      fitting_strategy=FITTING_STRATEGY,
                      max_job_size=MAX_JOB_SIZE,
                      buffer_size=BUFFER_SIZE)

    job_generator = JobGenerator(timer, cluster, comm_sensitive_percentage=comm_sensitivity_percentage, crop=CROP)

    cluster.update_job_queue(job_generator.draw_jobs(15000))

    utilizations = []
    jobs_in_queue = []
    needed_nodes = []
    taken_nodes = []
    first_job_in_queue_id = []
    backfilled_jobs_ids = []

    while cluster.work_to_do() and ITERATIONS > 0:
        cluster.run_time_tick()
        utilizations.append(cluster.count_cluster_utilization())
        logging.info('Utilization: {}'.format(utilizations[-1]))

        jobs_in_queue.append(len(cluster.job_queue.job_list))
        needed_nodes.append(sum([job.nodes_needed for job in cluster.running_jobs]))
        taken_nodes.append(np.count_nonzero(cluster._node_matrix))
        first_job_in_queue_id.append(cluster.job_queue.peek_at_first_job().job_id)
        backfilled_jobs_ids.append([(job.job_id, job.start_time) for job in cluster.backfill_jobs])
        logging.info('TIME: {}'.format(timer.time()))
        ITERATIONS -= 1

        if len(cluster.job_queue) <= 8000:
            cluster.update_job_queue(job_generator.draw_jobs(7000))

    logging.info('UTILIZATION_LIST: {} for minimal_bin_size: {} and comm_sensitivity_percentage: {}'.format(utilizations, minimal_bin_size, comm_sensitivity_percentage))
    logging.info('UTILIZATION_MEAN: {} for minimal_bin_size: {} and comm_sensitivity_percentage: {}'.format(np.mean(utilizations), minimal_bin_size, comm_sensitivity_percentage))

    # cluster.queue_size_plotter.preserve_window()

if __name__ == "__main__":
    logging.basicConfig(level=LOGGING_LEVEL)
    logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\nRUNNING SIMULATION FOR minimal_bin_size={}'
                 ' and comm_sensitivity_percentage: {}, backfilling {}, crop {}, size halved, {}'
                 ', buffer size: {}, max_job_size: {}'.format(1, 100, BACKFILLING_LEVEL, CROP, FITTING_STRATEGY,
                                                              BUFFER_SIZE, MAX_JOB_SIZE))
    main(1, 100)

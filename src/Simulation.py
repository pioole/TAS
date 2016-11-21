from src.JobGenerator import JobGenerator
from src.Cluster import Cluster
from src.Timer import Timer
from src.geometry_utils import Point3D

CLUSTER_SIDE_LENGTH = 24


def main():

    cluster_size = Point3D(CLUSTER_SIDE_LENGTH, CLUSTER_SIDE_LENGTH, CLUSTER_SIDE_LENGTH)

    cluster = Cluster(cluster_size)

    timer = Timer()

    job_generator = JobGenerator(timer, cluster)

    cluster.update_job_queue(job_generator.draw_jobs(5000))

    while cluster.work_to_do():
        cluster.run_time_tick()
        timer.tick()
        print 'TIME: {}'.format(timer.time())

    cluster.queue_size_plotter.preserve_window()

if __name__ == "__main__":
    main()


class Job(object):
    def __init__(self, job_id, work_time, nodes_needed, comm_sensitive, timer):
        """
        creates a new Job object
        :param job_id: Int: must be unique
        :param work_time: Int: time in "minutes"
        :param nodes_needed: Int
        :param comm_sensitive: Int: 1 - job is communication sensitive, 0 - is not
        :param timer: must have .time() method returning number of "minutes" from the start of the simulation
        :return: Job
        """
        self.job_id = job_id
        self.work_time = work_time
        self.nodes_needed = nodes_needed
        self.comm_sensitive = comm_sensitive
        self.start_time = None
        self.timer = timer

    def start_job(self):
        self.start_time = self.timer.time()

    def completed(self):
        try:
            return self.timer.time() - self.start_time > self.work_time
        except TypeError:
            return False  # Job not started

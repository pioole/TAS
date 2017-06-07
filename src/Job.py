

class Job(object):
    def __init__(self, job_id, work_time, nodes_needed, comm_sensitive, timer, cluster):
        """
        creates a new Job object
        :param job_id: Int: must be unique
        :param work_time: Int: time in "minutes"
        :param nodes_needed: Int
        :param comm_sensitive: Int: 1 - job is communication sensitive, 0 - is not
        :param timer: must have .time() method returning number of "minutes" from the start of the simulation
        :param cluster: a pointer to the cluster object
        :return: Job
        """
        self.job_id = job_id
        self.work_time = work_time
        self.nodes_needed = nodes_needed
        self.comm_sensitive = comm_sensitive
        self.start_time = None
        self.timer = timer
        self.cluster = cluster
        self.node_list = []

    def __str__(self):
        return 'Job id: {} size:{} work_time: {} nodes:{}'.format(self.job_id,
                                                                  self.nodes_needed, self.work_time, self.node_list)

    def __repr__(self):
        return self.__str__()

    def start_job(self):
        self.start_time = self.timer.time()

    def completed(self):
        try:
            return self.timer.time() - self.start_time > self.work_time
        except TypeError:
            return False  # Job not started

    def posess_nodes(self, node_list):
        """
        marks nodes given in the node_list as used by this job.
        :param node_list: [Job]
        :return: None
        """
        self.node_list = node_list
        self.cluster.assign_nodes(self.job_id, node_list, self)

    def free_nodes(self):
        """
        marks the nodes used by this job as not used.
        :return: None
        """
        self.cluster.free_nodes(self.job_id, self.node_list)

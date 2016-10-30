

class Job(object):
    def __init__(self, job_id, work_time, nodes_needed, comm_sensitive):
        self.job_id = job_id
        self.work_time = work_time
        self.nodes_needed = nodes_needed
        self.comm_sensitive = comm_sensitive

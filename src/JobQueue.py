

class JobQueue(object):
    def __init__(self):
        """
        initiates empty job list.
        :return: None
        """
        self.job_list = []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def fill_queue_with_jobs(self, job_list):
        """
        extends actual job queue with the given list of jobs
        :param job_list: [Job]
        :return: None
        """
        self.job_list.extend(job_list)

    def pop_first(self):
        """
        Returns the first job from the queue and removes it from queue.
        :return: Job
        """
        return self.job_list.pop(0)

    def peek_at_first_job(self):
        """
        Returns the first job from the queue without removing it.
        :return: Job
        """
        return self.job_list[0]

    def __len__(self):
        return len(self.job_list)

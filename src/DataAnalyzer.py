import os

from datetime import datetime, timedelta
import numpy as np

DEFAULT_JOB_DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def main():
    cluster_size_xe = 22500
    cluster_size_xk = 4200

    with open(os.path.join(DEFAULT_JOB_DATA_DIRECTORY, 'data_orig.csv')) as f:
        jobs_raw = f.readlines()
        jobs = []
        for raw_job in jobs_raw:
            job_splitted = raw_job.split(',')
            start_time_year = int(job_splitted[4].split('.')[-1])
            start_time_month = int(job_splitted[4].split('.')[-2])
            start_time_day = int(job_splitted[4].split('.')[-3][1:])
            start_time_hour = int(job_splitted[5].split(':')[0])
            start_time_minute = int(job_splitted[5].split(':')[1][:-1])
            start_time = datetime(start_time_year, start_time_month, start_time_day, start_time_hour, start_time_minute)
            end_time_year = int(job_splitted[6].split('.')[-1])
            end_time_month = int(job_splitted[6].split('.')[-2])
            end_time_day = int(job_splitted[6].split('.')[-3][1:])
            end_time_hour = int(job_splitted[7].split(':')[0])
            end_time_minute = int(job_splitted[7].split(':')[1][:-1])
            end_time = datetime(end_time_year, end_time_month, end_time_day, end_time_hour, end_time_minute)
            jobs.append((start_time, end_time, int(job_splitted[9]), job_splitted[10]))
        start_time = min(jobs, key=lambda x: x[0])[0]
        end_time = max(jobs, key=lambda x: x[1])[1]

        print 'start: ', start_time
        print 'end: ', end_time

        xe_list = []
        xk_list = []
        percentage_list_xe = []
        percentage_list_xk = []
        percentage_list = []

        while start_time < end_time:
            start_time += timedelta(minutes=5)
            nodes_running_xe = 0
            nodes_running_xk = 0
            for job in jobs:
                if job[0] <= start_time <= job[1]:
                    if job[3] == 'xe':
                        nodes_running_xe += job[2]
                    else:
                        nodes_running_xk += job[2]

            xe_list.append(nodes_running_xe)
            xk_list.append(nodes_running_xk)
            percentage_list_xe.append(100.*nodes_running_xe/cluster_size_xe)
            percentage_list_xk.append(100.*nodes_running_xk/cluster_size_xk)
            percentage_list.append(100.*(nodes_running_xk + nodes_running_xe)/(cluster_size_xk + cluster_size_xe))
            print 'time: {}, nodes running xe: {}, nodes running xk: {}, utilization_xe: {}%, utilization_xk: {}%, utilization_whole: {}%'.format(start_time,
                                                                                                     nodes_running_xe,
                                                                                                     nodes_running_xk,
                                                                                                     percentage_list_xe[-1],
                                                                                                     percentage_list_xk[-1],
                                                                                                     percentage_list[-1])

        print 'Mean xk: {}, mean xe: {}, utilization mean: {}%'.format(np.mean(xk_list), np.mean(xe_list), np.mean(percentage_list))
        print 'utilization xe mean: {}%, utilization xk mean: {}%'.format(np.mean(percentage_list_xe), np.mean(percentage_list_xk))

        for x in xrange(0, 100, 10):
            sum_ = 0
            for xe in percentage_list_xe:
                if x <= xe < x + 10:
                    sum_ += 1
            print '{}, {}'.format(x, sum_)




if __name__ == '__main__':
    main()

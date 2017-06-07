import os

DEFAULT_JOB_DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def main():
    with open(os.path.join(DEFAULT_JOB_DATA_DIRECTORY, 'data_orig.csv')) as f:
        jobs_raw = f.readlines()
    for x in xrange(11):
        with open(os.path.join(DEFAULT_JOB_DATA_DIRECTORY, 'data_{}.csv'.format(x*10)), 'w+') as f:
            counter = 0
            for job in jobs_raw:
                counter += 1
                if counter % 10 in xrange(x):
                    senn = 1
                else:
                    senn = 0
                f.write('{},'.format(senn) + job)


if __name__ == '__main__':
    main()

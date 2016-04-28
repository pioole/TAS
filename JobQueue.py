from SampleJob import SampleJob
import random


class JobQueue(object):
    def __init__(self, quantity=5000):
        # quantity is the number of sample jobs in this queue, defaultly it is 5000
        # list is the job queue that contains all sample jobs
        self.quantity = quantity
        self.list = []

    def QueryGenerate(self, flag=0):
        # generate quantity number of sample jobs in queue
        # sizelist was used to generate random size that used to generate sample jobs
        sizelist = 3679 * [1]
        my_randoms = [random.choice(xrange(2, 10)) for _ in range(876)]
        sizelist += my_randoms
        my_randoms = [random.choice(xrange(10, 50)) for _ in range(273)]
        sizelist += my_randoms
        my_randoms = [random.choice(xrange(50, 101)) for _ in range(172)]
        sizelist += my_randoms
        random.shuffle(sizelist)

        # timelist was used to generate random time that used to generate sample jobs
        timelist = []
        range_list = [(1, 61, 2407), (61, 121, 465), (121, 181, 93), (181, 241, 84), (241, 301, 190), (301, 361, 123),
                      (361, 421, 75), (421, 481, 61), (481, 541, 90), (541, 601, 93), (601, 661, 68), (661, 721, 50),
                      (721, 781, 47), (781, 841, 33), (841, 901, 50), (901, 961, 37), (961, 1021, 68),
                      (1021, 1081, 106), (1081, 1141, 131), (1141, 1201, 107), (1201, 1261, 85), (1261, 1321, 109),
                      (1321, 1381, 104), (1381, 1441, 324)
                      ]

        for range_input in range_list:
            my_randoms = [random.choice(xrange(range_input[0], range_input[1])) for _ in range(range_input[2])]
            timelist += my_randoms

        random.shuffle(timelist)

        for i in xrange(5000):
            if flag == 0 or flag == 1:
                newjob = SampleJob(i + 1, timelist[i], sizelist[i], flag)
                self.list.append(newjob)
            else:
                newjob = SampleJob(i + 1, timelist[i], sizelist[i], random.randint(0, 1))
                self.list.append(newjob)

        return self.list

    def pop(self):
        return self.list.pop()


q1 = JobQueue()
# print len(q1.QueryGenerate(3))
# print q1.list[1010].returnFlag()

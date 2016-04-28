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
        my_randoms = [random.choice(xrange(1, 61)) for _ in range(2407)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(61, 121)) for _ in range(465)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(121, 181)) for _ in range(93)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(181, 241)) for _ in range(84)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(241, 301)) for _ in range(190)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(301, 361)) for _ in range(123)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(361, 421)) for _ in range(75)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(421, 481)) for _ in range(61)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(481, 541)) for _ in range(90)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(541, 601)) for _ in range(93)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(601, 661)) for _ in range(68)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(661, 721)) for _ in range(50)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(721, 781)) for _ in range(47)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(781, 841)) for _ in range(33)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(841, 901)) for _ in range(50)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(901, 961)) for _ in range(37)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(961, 1021)) for _ in range(68)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1021, 1081)) for _ in range(106)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1081, 1141)) for _ in range(131)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1141, 1201)) for _ in range(107)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1201, 1261)) for _ in range(85)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1261, 1321)) for _ in range(109)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1321, 1381)) for _ in range(104)]
        timelist += my_randoms
        my_randoms = [random.choice(xrange(1381, 1441)) for _ in range(324)]
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

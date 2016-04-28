import numpy as np
from MaxRecSize import mul, max_size
from JobQueue import JobQueue

time = 0
running_process = []
side = 0
utilization = []


class NodeCluster(object):
    def __init__(self, input):
        """initial a 3d array with all 0 number included"""
        global side
        side = input
        self.side_number = input
        self.matrix = np.zeros((side, side, side))

    def get_matrix(self):
        """return the matrix"""
        return self.matrix

    def get_value(self, x, y, z):
        """return the"""
        return self.matrix[x, y, z]

    def set_value(self, x, y, z, value):
        """change one point in matrix to be a value we want"""
        self.matrix[x, y, z] = value

    def get_max_cuboid(self):
        """in 3d dimensions to get the largest Cuboid inside"""
        mat_list = self.matrix
        max_vol = 0
        max_area = 0
        max_index = 0
        level = 1
        while len(mat_list) > 0:
            for index, each in enumerate(mat_list):
                if reduce(mul, max_size(each)[0]) * level > max_vol:
                    max_vol = reduce(mul, max_size(each)[0]) * level
                    max_area = max_size(each)
                    max_index = [index, level]
            mat_list = self.generate_overlapped_set(mat_list)
            level += 1
        return {"maxvol": max_vol, "maxarea": max_area, "maxindex": max_index}

    def generate_overlapped_set(self, mat1):
        """get the overlapped matrix by mat1"""
        temp_mat = np.zeros((len(mat1) - 1, self.side_number, self.side_number))
        for i in xrange(len(mat1) - 1):
            for x in xrange(self.side_number):
                for y in xrange(self.side_number):
                    val = mat1[i, x, y] or mat1[i + 1, x, y]
                    temp_mat[i, x, y] = val

        return temp_mat

    def get_max_subsets(self):
        """get the largest subset matrix from each single matrix"""
        max_matrix_list = []
        for i in xrange(len(self.matrix)):
            max_matrix_list.append({"index": i, "matrix": max_size(self.matrix[i])})

        max_matrix_list = sorted(max_matrix_list, key=lambda mat: reduce(mul, mat["matrix"][0]), reverse=True)
        return max_matrix_list

    def insert_to_max_cuboid(self, queue):
        global time
        global running_process
        global utilization

        max_cuboid = self.get_max_cuboid()
        start_index = max_cuboid["maxindex"][0]
        end_index = max_cuboid["maxindex"][0] + max_cuboid["maxindex"][1] - 1

        mat = max_cuboid["maxarea"]
        start_cood_x = mat[1] + 1 - mat[0][0]
        start_cood_y = mat[2]
        end_cood_x = mat[1]
        end_cood_y = mat[3]
        row_length = mat[0][0]
        col_length = mat[0][1]

        cood_list = []
        for x in xrange(start_cood_x, end_cood_x + 1):
            for y in xrange(start_cood_y, end_cood_y + 1):
                cood_list.append([x, y])

        head_start_i = 0
        head_end_i = len(cood_list) - 1

        tail_start_i = 0
        tail_end_i = len(cood_list) - 1
        print "tailendi originally = " + str(tail_end_i)

        while True:

            if len(queue) > 0:
                current_job = queue[len(queue) - 1]
                print "length of queue" + str(len(queue))
            else:
                print "Queue is empty"
                break

            job_size = current_job.returnSize()

            if start_index < end_index:

                if current_job.returnFlag() == 1:

                    # start to check if we can place the job into the matrix
                    if job_size % col_length != 0:
                        required_space = (job_size / col_length + 1) * col_length
                    else:
                        required_space = job_size

                    if required_space <= head_end_i - head_start_i + 1:
                        # job can be placed in
                        cood = []
                        for i in xrange(head_start_i, head_start_i + job_size):
                            self.matrix[start_index, cood_list[i][0], cood_list[i][1]] = current_job.returnId()
                            cood.append([start_index, cood_list[i][0], cood_list[i][1]])
                        if job_size % col_length != 0:
                            for i in xrange(head_start_i + job_size, head_start_i + (job_size / col_length + 1) * col_length):
                                self.matrix[start_index, cood_list[i][0], cood_list[i][1]] = -current_job.returnId()
                                cood.append([start_index, cood_list[i][0], cood_list[i][1]])
                            head_start_i = head_start_i + (job_size / col_length + 1) * col_length
                        else:
                            head_start_i = head_start_i + job_size
                        end_time = time + current_job.returnTime()
                        running_process.append({"coodinate": cood, "endtime": end_time})
                        queue.pop()

                    else:
                        # job cannot be placed in
                        head_start_i = 0
                        start_index += 1

                        if start_index == end_index:
                            head_end_i = tail_end_i

                else:  # currentjob.returnFlag() == 0

                    required_space = job_size

                    if required_space <= tail_end_i - tail_start_i + 1:  # job can be placed in
                        cood = []
                        for i in xrange(tail_end_i - job_size + 1, tail_end_i + 1):
                            self.matrix[end_index, cood_list[i][0], cood_list[i][1]] = current_job.returnId()
                            cood.append([end_index, cood_list[i][0], cood_list[i][1]])
                        tail_end_i = tail_end_i - job_size
                        end_time = time + current_job.returnTime()
                        running_process.append({"coodinate": cood, "endtime": end_time})
                        queue.pop()
                    else:  # job cannot be placed in
                        tail_end_i = len(cood_list) - 1
                        end_index -= 1

                        if start_index == end_index:
                            tail_start_i = head_start_i

            if start_index == end_index:

                if current_job.returnFlag() == 1:

                    ava_space = (head_end_i - head_start_i + 1) / col_length * col_length
                    if job_size % col_length == 0:
                        required_space = job_size
                    else:
                        required_space = (job_size / col_length + 1) * col_length

                    print "avaspace" + str(ava_space)
                    print "requiredspace" + str(required_space)

                    if ava_space >= required_space:  # job can be put in
                        cood = []
                        print "headstarti" + str(tail_end_i)
                        print "startindex" + str(start_index)
                        print "endindex" + str(end_index)
                        for i in xrange(head_start_i, head_start_i + job_size):
                            self.matrix[start_index, cood_list[i][0], cood_list[i][1]] = current_job.returnId()
                            cood.append([start_index, cood_list[i][0], cood_list[i][1]])
                        if job_size % col_length != 0:
                            for i in xrange(head_start_i + job_size, head_start_i + (job_size / col_length + 1) * col_length):
                                self.matrix[start_index, cood_list[i][0], cood_list[i][1]] = -current_job.returnId()
                                cood.append([start_index, cood_list[i][0], cood_list[i][1]])
                            head_start_i = head_start_i + (job_size / col_length + 1) * col_length
                            tail_start_i = head_start_i
                        else:
                            head_start_i = head_start_i + job_size
                            tail_start_i = head_start_i
                        end_time = time + current_job.returnTime()
                        running_process.append({"coodinate": cood, "endtime": end_time})
                        queue.pop()

                    else:  # job cannot be put in
                        print "cannot insert More add time"
                        print self.cal_utilization()
                        print self.matrix[0]
                        print self.matrix[1]
                        print self.matrix[20]
                        utilization.append({"time": time, "util": self.cal_utilization()})
                        time += 50
                        break

                else:

                    ava_space = tail_end_i - tail_start_i + 1
                    print "avaspace" + str(ava_space)
                    required_space = job_size
                    print "requiredspace" + str(required_space)

                    if ava_space >= required_space:  # job can be put in
                        cood = []
                        print "tailendi" + str(tail_end_i)
                        print "startindex" + str(start_index)
                        print "endindex" + str(end_index)

                        for i in xrange(tail_end_i - job_size + 1, tail_end_i + 1):
                            print i
                            self.matrix[end_index, cood_list[i][0], cood_list[i][1]] = current_job.returnId()
                            cood.append([end_index, cood_list[i][0], cood_list[i][1]])
                        tail_end_i = tail_end_i - job_size
                        head_end_i = tail_end_i
                        end_time = time + current_job.returnTime()
                        running_process.append({"coodinate": cood, "endtime": end_time})
                        queue.pop()

                    else:  # job cannot be put in
                        print "cannot insert More add time"
                        print self.cal_utilization()
                        print self.matrix[0]
                        print self.matrix[1]
                        print self.matrix[20]
                        utilization.append({"time": time, "util": self.cal_utilization()})
                        time += 50
                        break

        for each in running_process:
            if each["endtime"] <= time:
                for cood in each["coodinate"]:
                    self.matrix[cood[0], cood[1], cood[2]] = 0
                running_process.remove(each)

        return queue

    def insert_to_max_subset(self, queue):
        global time
        global running_process
        global utilization

        max_matrix_list = self.get_max_subsets()
        max_area = reduce(mul, max_matrix_list[0]["matrix"][0])
        index = max_matrix_list[0]["index"]
        mat = max_matrix_list[0][
            "matrix"]  # mat is in the format : [(rowlength, collength), lastrownum, startcolnum, endcolnumber]
        start_cood_x = mat[1] + 1 - mat[0][0]
        start_cood_y = mat[2]
        end_cood_x = mat[1]
        end_cood_y = mat[3]
        row_length = mat[0][0]
        col_length = mat[0][1]

        cood_list = []
        for x in xrange(start_cood_x, end_cood_x + 1):
            for y in xrange(start_cood_y, end_cood_y + 1):
                cood_list.append([x, y])

        start_i = 0
        end_i = len(cood_list) - 1

        while True:

            if len(queue) > 0:
                current_job = queue[len(queue) - 1]
            else:
                break
            job_size = current_job.returnSize()

            if job_size <= end_i - start_i + 1:

                queue.pop()

                if current_job.returnFlag() == 1:
                    cood = []
                    for i in xrange(start_i, start_i + job_size):
                        self.matrix[index, cood_list[i][0], cood_list[i][1]] = current_job.returnId()
                        cood.append([index, cood_list[i][0], cood_list[i][1]])
                    if job_size % col_length != 0:
                        for i in xrange(start_i + job_size, start_i + (job_size / col_length + 1) * col_length):
                            self.matrix[index, cood_list[i][0], cood_list[i][1]] = -current_job.returnId()
                            cood.append([index, cood_list[i][0], cood_list[i][1]])
                        start_i = start_i + (job_size / col_length + 1) * col_length
                    else:
                        start_i = start_i + job_size
                    end_time = time + current_job.returnTime()
                    running_process.append({"coodinate": cood, "endtime": end_time})

                else:
                    cood = []
                    for i in xrange(end_i - job_size + 1, end_i + 1):
                        self.matrix[index, cood_list[i][0], cood_list[i][1]] = current_job.returnId()
                        cood.append([index, cood_list[i][0], cood_list[i][1]])
                    end_i = end_i - job_size
                    end_time = time + current_job.returnTime()
                    running_process.append({"coodinate": cood, "endtime": end_time})

            else:
                if job_size > reduce(mul, self.get_max_subsets()[0]["matrix"][0]):
                    print "cant insert anymore"
                    print time
                    # file.write("time: "+str(time)+", jobsize: "+str(jobsize)+", maxsubmatrix: "+str(reduce(mul, self.get_max_subsets()[0]["matrix"][0]))+"\n" )
                    for i in xrange(side):
                        reshapedmatrix = np.asarray(self.matrix[i]).reshape(-1)
                        # file.write(str(reshapedmatrix))
                    # file.write("\n")
                    utilization.append({"time": time, "util": self.cal_utilization()})
                    time += 50
                break

        for each in running_process:
            if each["endtime"] <= time:
                for cood in each["coodinate"]:
                    self.matrix[cood[0], cood[1], cood[2]] = 0
                running_process.remove(each)

        # file.close()
        return queue

    def cal_utilization(self):
        count = 0
        for x in xrange(side):
            for y in xrange(side):
                for z in xrange(side):
                    if self.matrix[x, y, z] != 0:
                        count += 1
        percentage = float(count) / float(side * side * side)
        return percentage


def main():
    a = NodeCluster(24)
    print a.cal_utilization()
    # print(a.get_value(2,4,5))
    q1 = JobQueue()
    q = q1.generate_query(3)

    while len(q) > 0:
        q = a.insert_to_max_cuboid(q)

    with open('result0', 'w') as f:
        for each in utilization:
            time = each['time']
            util = each['util']
            f.write('{},{}\n'.format(str(time), str(util)))

    print a.get_max_cuboid()
    print running_process

if __name__ == "__main__":
    main()



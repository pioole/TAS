from numpy import *
from MaxRecSize import *
from SampleJob import SampleJob
from JobQueue import JobQueue

time = 0
runningprocess = []
side = 0
utilization = []

class NodeCluster(object):
    def __init__(self, input):
    # initial a 3d array with all 0 number included
        #self.matrix = [[[0 for x in range(side)] for x in range(side)] for x in range(side)]
        global side
        side = input
        self.sidenumber = input
        self.matrix = zeros((side, side, side))

    def returnMatrix(self):
    # return the matrix
        return self.matrix

    def returnValue(self, x, y, z):
    # return the 
        return self.matrix[x,y,z]

    def changeValue(self, x, y, z, value):
    # change one point in matrix to be a value we want
        self.matrix[x,y,z] = value



    def getMaxCuboid(self):
    # in 3d dimensions to get the largest Cuboid inside
        matlist = self.matrix
        maxvol = 0
        maxarea = 0
        maxindex = 0
        level = 1
        while len(matlist)>0:
            for index, each in enumerate(matlist):
                if reduce(mul, max_size(each)[0])*level>maxvol:
                    maxvol = reduce(mul, max_size(each)[0])*level
                    maxarea = max_size(each)
                    maxindex = [index, level]
            matlist = self.generateOverlappedSet(matlist)
            level+=1
        return {"maxvol": maxvol, "maxarea":maxarea, "maxindex":maxindex}


            
    def generateOverlappedSet(self, mat1):
    # get the overlapped matrix by mat1
        tempmat = zeros((len(mat1)-1,self.sidenumber,self.sidenumber))
        for i in xrange(len(mat1)-1):
            for x in xrange(self.sidenumber):
                for y in xrange(self.sidenumber):
                    val = mat1[i,x,y] or mat1[i+1,x,y]
                    tempmat[i,x,y] = val

        return tempmat
            


    def getMaxSubsets(self):
    # get the largest subset matrix from each single matrix
        maxmatrixlist = []
        for i in xrange(len(self.matrix)):
            maxmatrixlist.append({"index": i, "matrix":max_size(self.matrix[i])})

        maxmatrixlist = sorted(maxmatrixlist, key= lambda mat: reduce(mul, mat["matrix"][0]), reverse=True)
        return maxmatrixlist




    def insertToMaxCuboid(self, queue):
        global time
        global runningprocess
        global utilization

        maxcuboid = self.getMaxCuboid()
        startindex = maxcuboid["maxindex"][0]
        endindex = maxcuboid["maxindex"][0] + maxcuboid["maxindex"][1]-1

        mat = maxcuboid["maxarea"]
        startcoodx = mat[1]+1 - mat[0][0]
        startcoody = mat[2]
        endcoodx = mat[1]
        endcoody = mat[3]
        rowlength = mat[0][0]
        collength = mat[0][1]

        coodlist = []
        for x in xrange(startcoodx, endcoodx+1):
            for y in xrange(startcoody, endcoody+1):
                coodlist.append([x,y])

        headstarti = 0 
        headendi = len(coodlist)-1

        tailstarti = 0
        tailendi = len(coodlist)-1
        print "tailendi originally = "+str(tailendi)

        while True:

            if len(queue) > 0:
                    currentjob = queue[len(queue)-1]
                    print "length of queue"+str(len(queue))
            else:
                print "Queue is empty"
                break


            jobsize = currentjob.returnSize()


            if startindex < endindex:

                if currentjob.returnFlag() == 1 :

                    # start to check if we can place the job into the matrix
                    if jobsize % collength != 0:
                        requiredspace = (jobsize/collength+1)*collength
                    else:
                        requiredspace = jobsize

                    if  requiredspace <= headendi - headstarti + 1 :
                    # job can be placed in
                        cood = []
                        for i in xrange(headstarti, headstarti+jobsize):
                            self.matrix[startindex, coodlist[i][0], coodlist[i][1]] = currentjob.returnId()
                            cood.append([startindex, coodlist[i][0], coodlist[i][1]])
                        if jobsize%collength != 0:
                            for i in xrange(headstarti+jobsize, headstarti+(jobsize/collength+1)*collength):
                                self.matrix[startindex, coodlist[i][0], coodlist[i][1]] = -currentjob.returnId()
                                cood.append([startindex, coodlist[i][0], coodlist[i][1]])
                            headstarti = headstarti+(jobsize/collength+1)*collength
                        else:
                            headstarti = headstarti+jobsize
                        endtime = time + currentjob.returnTime()
                        runningprocess.append({"coodinate":cood,"endtime":endtime})
                        queue.pop()

                    else:
                    # job cannot be placed in
                        headstarti = 0
                        startindex += 1

                        if startindex == endindex:
                            headendi = tailendi


                else:# currentjob.returnFlag() == 0

                    requiredspace = jobsize

                    if requiredspace <= tailendi - tailstarti + 1:
                    # job can be placed in
                        cood = []
                        for i in xrange(tailendi-jobsize+1, tailendi+1):
                            self.matrix[endindex, coodlist[i][0], coodlist[i][1]] = currentjob.returnId()
                            cood.append([endindex, coodlist[i][0], coodlist[i][1]])
                        tailendi = tailendi - jobsize
                        endtime = time + currentjob.returnTime()
                        runningprocess.append({"coodinate":cood,"endtime":endtime})
                        queue.pop()
                    else:
                    # job cannot be placed in
                        tailendi = len(coodlist)-1
                        endindex -= 1

                        if startindex == endindex:
                            tailstarti = headstarti

            if startindex == endindex:

                if currentjob.returnFlag() == 1:

                    avaspace = (headendi - headstarti + 1)/collength * collength
                    if jobsize % collength == 0:
                        requiredspace = jobsize
                    else:
                        requiredspace = (jobsize/collength + 1)*collength

                    print "avaspace"+str(avaspace)
                    print "requiredspace"+str(requiredspace)

                    if avaspace >= requiredspace: # job can be put in
                        cood = []
                        print "headstarti"+str(tailendi)
                        print "startindex"+str(startindex)
                        print "endindex"+str(endindex)
                        for i in xrange(headstarti, headstarti+jobsize):
                            self.matrix[startindex, coodlist[i][0], coodlist[i][1]] = currentjob.returnId()
                            cood.append([startindex, coodlist[i][0], coodlist[i][1]])
                        if jobsize%collength != 0:
                            for i in xrange(headstarti+jobsize, headstarti+(jobsize/collength+1)*collength):
                                self.matrix[startindex, coodlist[i][0], coodlist[i][1]] = -currentjob.returnId()
                                cood.append([startindex, coodlist[i][0], coodlist[i][1]])
                            headstarti = headstarti+(jobsize/collength+1)*collength
                            tailstarti = headstarti
                        else:
                            headstarti = headstarti+jobsize
                            tailstarti = headstarti
                        endtime = time + currentjob.returnTime()
                        runningprocess.append({"coodinate":cood,"endtime":endtime})
                        queue.pop()

                    else: # job cannot be put in
                        # sort runningprocess by endtime from small to large, go to the smallest
                        print "cannot insert More add time"
                        print self.calUtilization()
                        print self.matrix[0]
                        print self.matrix[1]
                        print self.matrix[20]
                        #runningprocess = sorted(runningprocess, key= lambda p: p["endtime"])
                        utilization.append({"time":time,"util":self.calUtilization()})
                        #time = runningprocess[0]["endtime"]
                        time += 50
                        break

                else:

                    avaspace = tailendi - tailstarti + 1
                    print "avaspace"+str(avaspace)
                    requiredspace = jobsize
                    print "requiredspace"+str(requiredspace)

                    if avaspace >= requiredspace: # job can be put in
                        cood = []
                        print "tailendi"+str(tailendi)
                        print "startindex"+str(startindex)
                        print "endindex"+str(endindex)

                        for i in xrange(tailendi-jobsize+1, tailendi+1):
                            print i
                            self.matrix[endindex, coodlist[i][0], coodlist[i][1]] = currentjob.returnId()
                            cood.append([endindex, coodlist[i][0], coodlist[i][1]])
                        tailendi = tailendi - jobsize
                        headendi = tailendi
                        endtime = time + currentjob.returnTime()
                        runningprocess.append({"coodinate":cood,"endtime":endtime})
                        queue.pop()

                    else: # job cannot be put in
                        # sort runningprocess by endtime from small to large, go to the smallest
                        print "cannot insert More add time"
                        print self.calUtilization()
                        print self.matrix[0]
                        print self.matrix[1]
                        print self.matrix[20]
                        #runningprocess = sorted(runningprocess, key= lambda p: p["endtime"])
                        utilization.append({"time":time,"util":self.calUtilization()})
                        #time = runningprocess[0]["endtime"]
                        time += 50
                        break

        for each in runningprocess:
            if each["endtime"] <= time:
                for cood in each["coodinate"]:
                     self.matrix[cood[0], cood[1], cood[2]] = 0
                runningprocess.remove(each)

        return queue

    def insertToMaxSubset(self, queue):
        global time
        global runningprocess
        global utilization

        maxmatrixlist = self.getMaxSubsets()
        maxarea = reduce(mul, maxmatrixlist[0]["matrix"][0])
        index = maxmatrixlist[0]["index"]
        mat = maxmatrixlist[0]["matrix"] # mat is in the format : [(rowlength, collength), lastrownum, startcolnum, endcolnumber]
        startcoodx = mat[1]+1 - mat[0][0]
        startcoody = mat[2]
        endcoodx = mat[1]
        endcoody = mat[3]
        rowlength = mat[0][0]
        collength = mat[0][1]

        coodlist = []
        for x in xrange(startcoodx, endcoodx+1):
            for y in xrange(startcoody, endcoody+1):
                coodlist.append([x,y])
        
        #print len(coodlist)
        starti = 0 
        endi = len(coodlist)-1

        #file = open("matrix","a")
        while True:

            if len(queue) > 0:
                    currentjob = queue[len(queue)-1]
            else:
                break
            #print currentjob
            #print "id:"+str(currentjob.returnId())
            #print "flag:"+str(currentjob.returnFlag())
            #print "size:"+str(currentjob.returnSize())
            #print "runtime:"+str(currentjob.returnTime())
            jobsize = currentjob.returnSize()
            #print "endi:"+str(endi)
            #print "starti:"+str(starti)
            #print "time:"+str(time)


            if jobsize <= endi-starti+1:

                queue.pop()

                if currentjob.returnFlag() == 1:
                    cood = []
                    for i in xrange(starti, starti+jobsize):
                        self.matrix[index, coodlist[i][0], coodlist[i][1]] = currentjob.returnId()
                        cood.append([index, coodlist[i][0], coodlist[i][1]])
                    if jobsize%collength != 0:
                        for i in xrange(starti+jobsize, starti+(jobsize/collength+1)*collength):
                            self.matrix[index, coodlist[i][0], coodlist[i][1]] = -currentjob.returnId()
                            cood.append([index, coodlist[i][0], coodlist[i][1]])
                        starti = starti+(jobsize/collength+1)*collength
                    else:
                        starti = starti+jobsize
                    endtime = time + currentjob.returnTime()
                    runningprocess.append({"coodinate":cood,"endtime":endtime})
                
                else:
                    cood = []
                    for i in xrange(endi-jobsize+1, endi+1):
                        self.matrix[index, coodlist[i][0], coodlist[i][1]] = currentjob.returnId()
                        cood.append([index, coodlist[i][0], coodlist[i][1]])
                    endi = endi - jobsize
                    endtime = time + currentjob.returnTime()
                    runningprocess.append({"coodinate":cood,"endtime":endtime})

            else:
                if jobsize > reduce(mul, self.getMaxSubsets()[0]["matrix"][0]):
                    print "cant insert anymore"
                    print time
                    #file.write("time: "+str(time)+", jobsize: "+str(jobsize)+", maxsubmatrix: "+str(reduce(mul, self.getMaxSubsets()[0]["matrix"][0]))+"\n" )
                    for i in xrange(side):
                        reshapedmatrix = asarray(self.matrix[i]).reshape(-1)
                        #file.write(str(reshapedmatrix))
                    #file.write("\n")
                    utilization.append({"time":time,"util":self.calUtilization()})
                    time += 50
                break

        for each in runningprocess:
            if each["endtime"] <= time:
                for cood in each["coodinate"]:
                     self.matrix[cood[0], cood[1], cood[2]] = 0
                runningprocess.remove(each)

        #file.close()
        return queue

    def calUtilization(self):
        count = 0
        for x in xrange(side):
            for y in xrange(side):
                for z in xrange(side):
                    if self.matrix[x,y,z] != 0:
                        count += 1
        percentage = float(count)/float(side*side*side)
        return percentage





#a = NodeCluster(24)
#print a.calUtilization()
#b = a.generateOverlappedSet(a.matrix)
#print a.getMaxCuboid()
#print len(b)
#print len(b[0])
#print b
#q1 = JobQueue()
#q = q1.QueryGenerate(3)

#while len(q) > 0:
#    q = a.insertToMaxSubset(q)

#f = open('result0','w')
#for each in utilization:
#   time = each['time']
#   util = each['util']
#   f.write(str(time)+","+str(util)+'\n') 
#f.close()


#print a.getMaxSubsets()
#print runningprocess

a = NodeCluster(24)
print a.calUtilization()
#print(a.returnValue(2,4,5))
q1 = JobQueue()
q = q1.QueryGenerate(3)

while len(q) > 0:
    q = a.insertToMaxCuboid(q)

f = open('result0','w')
for each in utilization:
    time = each['time']
    util = each['util']
    f.write(str(time)+","+str(util)+'\n') 
f.close() # you can omit in most cases as the destructor will call it


print a.getMaxCuboid()
print runningprocess
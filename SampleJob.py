
class SampleJob(object):
	def __init__(self, id=0 , time=0, size=0, flag=0):
	# id is the job id, time is how many mins the job will finish
	# size is the how many nodes the job requires, flag means if the job require rectang space.
		self.id = int(id)
		self.time = int(time)
		self.size = int(size)
		self.flag = int(flag)

	def returnId(self):
		return self.id

	def returnTime(self):
		return self.time

	def returnSize(self):
		return self.size

	def returnFlag(self):
		return self.flag

#job1 = SampleJob(1,2,3,1)
#print job1.returnFlag()
#print job1.returnTime()
#print job1.returnSize()
#print job1.returnId()
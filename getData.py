from PIL import Image
import os
import random
import numpy as np
class dataSet:	
	def __init__(self, dir):
		self.train_batch = 0
		self.test_batch = 0
		self.train_total_batch = 0
		self.test_total_batch = 0
		self.trainSet = []
		self.testSet = []
		self.trainLabel = []
		self.testLabel = []
		self.dir = dir
		self.initBatch()
	def initBatch(self):
		path = "./" + self.dir
		filelist = os.listdir(path)
		count = 0
		personNum = len(filelist)
		print "Num:",personNum
		zeros = [0 for i in range(personNum)]
		for person in filelist:
			print person,count
			localSet = []
			filedir = os.path.join(path, person)
			if os.path.isdir(filedir):
				childlist = os.listdir(filedir)
				 
				for image in childlist:
					imagedir = os.path.join(filedir,image)
					filetype = os.path.splitext(image)[1]
					if(filetype == '.png'):
						filein = Image.open(imagedir)
						data = filein.load()
						w = filein.size[0]
						h = filein.size[1]
						pic =[]
						for i in range(w):
							pic_w = []
							for j in range(h):
								pic_h =[data[i,j][0],data[i,j][1],data[i,j][2]]
								pic_w.append(pic_h)
							pic.append(pic_w)
						pic = np.array(pic)
						pic = pic - 127.5
						pic = pic/127.50
						pic = pic.tolist()
						localSet.append(pic)
									
			trainNum = int(len(localSet)*0.8)
			testNum = len(localSet) - trainNum
			for i in range(trainNum):
				self.trainSet.append(localSet[i])
				localZeros = [0 for i in range(personNum)]
				localZeros[count] = 1
				self.trainLabel.append(localZeros)
			for j in range(testNum):
				self.testSet.append(localSet[j + trainNum])
				localZeros = [0 for i in range(personNum)]
				localZeros[count] = 1
				self.testLabel.append(localZeros)
			self.train_total_batch += trainNum
			self.test_total_batch += testNum
			count = count+1
		to_be_shuffled = [ (self.trainSet[i],self.trainLabel[i]) for i in range(len(self.trainSet))]
		random.shuffle(to_be_shuffled)
		self.trainSet = [] 
		self.trainLabel = []
		for i in range(len(to_be_shuffled)):
			self.trainSet.append(to_be_shuffled[i][0])
			self.trainLabel.append(to_be_shuffled[i][1])
	def next_train_batch(self, num):
		ret = []
		image =[]
		label =[]
		for i in range(min(self.train_total_batch - self.train_batch, num)):
			image.append(self.trainSet[self.train_batch + i])
			label.append(self.trainLabel[self.train_batch + i])
		    	
		self.train_batch = (self.train_batch + len(ret)) % self.train_total_batch
		return [image,label]

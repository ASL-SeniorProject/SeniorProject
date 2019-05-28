"""
#
#            Letter Guesser
#                 for
#              ASL Unity
#
#             Written By
#            Nick Jackson
#             5/15/2019
#         
"""

"""
###
### EDIT LOG
###
### Nick Jackson - 5/15/2019
###
###
"""

from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.feature import *
from sklearn.neural_network import MLPClassifier as NN
from multiNetPictureProcess import *
from BlobFinder import *
import numpy as np
import pickle
import sys
import os
import random

"""
	Global Variables to mess with.
	Details for variables available in README
"""

# Guesser variables
guesserConstruction = "new"
guesserName = "blueBoostNet"
guesserType = "multi"

# Data range variables
dataSet = "blueHands"
dataType = "blueBoost"
startLetter = 'A'
endLetter = 'Z'
percentToUse = 100

# Netowrk construction variables
activationFunction = 'tanh'
solverAlgorithm = 'adam'
epochs = 500
hiddenLayers = (100,)

"""
	Global Variables to leave alone.

	maxMins stores the max and min values for each key point
coordinate in the input data. It uses these for normalization.
	data stores the input data for the guesser.
"""
maxMins = []
data = []

class Guesser(object):
	def __init__(self, type="multi", name="tempNet"):
		self.networks = []
		self.type = type
		self.name = name
		if type == "multi":
			for i in range(ord(endLetter) - ord(startLetter) + 1):
				self.networks.append(NN(hidden_layer_sizes=hiddenLayers, activation=activationFunction, solver=solverAlgorithm, max_iter=epochs))
		elif type == "mono":
			self.networks.append(NN(hidden_layer_sizes=hiddenLayers, activation=activationFunction, solver=solverAlgorithm, max_iter=epochs))
		else:
			print("Invalid type")
			sys.exit(1)
	
	def train(self):
		trainingDataX = []
		trainingDataY = []
		if self.type == "multi":
			for i in range(len(self.networks)):
				print("Training network: " + chr(i + ord('A')))
				trainingDataX = []
				trainingDataY = []
				for j in range(int(len(data[i]) * percentToUse/100)):
					trainingDataX.append(data[i][j])
					trainingDataY.append(1)
				if len(self.networks) > 1:
					for j in range(int(len(data[i]) * percentToUse/100) * 4):
						temp = random.randint(0,ord(endLetter) - ord(startLetter))
						while temp == i:
							temp = random.randint(0,ord(endLetter) - ord(startLetter))
						trainingDataX.append(data[temp][random.randint(0,len(data[temp])-1)])
						trainingDataY.append(0)
				self.networks[i].fit(trainingDataX, trainingDataY)
		elif self.type == "mono":
			for i in range(len(data)):
				for j in range(int(len(data[i]) * percentToUse/100)):
					trainingDataX.append(data[i][j])
					trainingDataY.append(i)
			self.networks[0].fit(trainingDataX, trainingDataY)
		else:
			print("Invalid network type")
			sys.exit(1)
	
	def predict(self, data):
		if self.type == "multi":
			yesList = []
			for i in range(len(self.networks)):
				if self.networks[i].predict(data)[0] == 1:
					yesList.append(i)
			return yesList
		elif self.type == "mono":
			return self.networks[0].predict(data)
		else:
			print("Invalid network type")
			sys.exit(1)

	def save(self):
		pickle.dump(self, open(self.name, "wb"))
	
def buildData():
	shapeM = np.array([[[0,0,1]]*50]*50)
	data = []
	for i in range(ord(endLetter)-ord(startLetter)+1):
		data.append([])
	for path, dirs, files in os.walk("./BlueHandAlphabet/Cropped"):
		if ord(path[-1]) >= ord(startLetter) and ord(path[-1]) <= ord(endLetter):
			for fname in files:
				if dataType == "xcanny":
					img = canny(rgb2gray(imread(path + "/" + fname)))
					img1D = []
					for i in range(len(img)):
						for j in range(len(img[i])):
							img1D.append(img[i][j])
					data[ord(path[-1]) - ord(startLetter)].append(img1D)
				elif dataType == "hog":
					data[ord(path[-1]) - ord(startLetter)].append(hog(rgb2gray(imread(path + "/" + fname))))
				elif dataType == "canny":
					img = canny(rgb2gray(imread(path + "/" + fname)))
					img1D = []
					for i in range(len(img)):
						img1D.append(float(np.sum(np.array(img[i])))/float(len(img[i])))
					data[ord(path[-1]) - ord(startLetter)].append(img1D)
				elif dataType == "tensor":
					img1D = []
					Axx, Axy, Ayy = structure_tensor(rgb2gray(imread(path + "/" + fname)), sigma=0.1)
					img2D = structure_tensor_eigvals(Axx, Axy, Ayy)[0]
					for obj in img2D:
						for el in obj:
							img1D.append(el)
					data[ord(path[-1]) - ord(startLetter)].append(img1D)
				elif dataType == "blueBoost":
					temp = imread(path + "/" + fname)*shapeM
					max = np.amax(temp)
					temp = temp / np.array([[[1,1,float(max)]]*50]*50)
					data[ord(path[-1]) - ord(startLetter)].append(temp.flatten()[2::3])
				else:
					print("Invalid data type, exiting")
					exit()
	return data

if __name__ == "__main__":
	# ----------------------------------
	# Verify some user input data ranges
	# ----------------------------------
	if percentToUse < 0 or percentToUse > 100:
		print("percentToUse has to be between 0 and 100")
		sys.exit(1)
	if ord(endLetter) < ord(startLetter):
		print("endLetter must come after, or be the same as, the alphabetical position of startLetter")
		sys.exit(1)
	
	# ---------------------------------------------
	# Initialize the maxMin arrays and prepare data
	# ---------------------------------------------
	"""
	for i in range(42):
		maxMins.append([0.0, 10000.0])
	"""
	data = buildData()
	
	# ---------------------------------------------
	# Construct the letter guesser for this session
	# ---------------------------------------------
	if guesserConstruction == "load":
		g = pickle.load(open("./" + guesserName, "rb"))
	elif guesserConstruction == "new":
		g = Guesser(type=guesserType, name=guesserName)
		g.train()
	else:
		print(guesserConstruction + " is an invalid value for guesserConstruction.")
		sys.exit(1)
	
	# ------------------------------------------------------------
	# Save the network for future use (this barely takes any time)
	# ------------------------------------------------------------
	g.save()
	
	# ----------------------------------
	# Check the accuracy of your network
	# ----------------------------------
	
	for i in range(len(data)):
		print(chr(i + ord('A')) + ": " + str(g.predict([data[i][i]])))
	
	for i in range(len(data)):
		temp = 0
		for j in range(len(data[i])):
			if g.type == "mono" and g.predict([data[i][j]])[0] == i:
				temp += 1
			elif g.type == "multi" and i in g.predict([data[i][j]]):
				temp += 1
		print(chr(i + ord('A')) + ": " + str(temp/len(data[i])))
	"""
	
	data = []
	img = imread("./TestC1.jpg")
	img = rgb2gray(resize(img, (200,200),anti_aliasing=True))
	for ent in canny(img):
		temp = 0
		for boo in ent:
			if boo:
				temp += 1
		data.append(float(temp)/float(len(ent)))
	print(g.predict([data]))
	"""
"""
#
#            Letter Guesser
#                 for
#              ASL Unity
#
#             Written By
#            Nick Jackson
#             4/12/2019
#         
"""

"""
###
### EDIT LOG
###
### Nick Jackson - 4/13/2019
###
###
"""

from sklearn.neural_network import MLPClassifier as NN
import pickle
import sys
import os
import random

"""
	Global Variables to mess with.
"""

# Guesser variables
guesserConstruction = "new"
guesserName = "YourCoolGuesser2"
guesserType = "mono"

# Data range variables
startLetter = 'A'
endLetter = 'C'
percentToUse = 100

# Netowrk construction variables
activationFunction = 'tanh'
solverAlgorithm = 'lbfgs'
epochs = 1000
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
				for j in range(int(len(data[i]) * percentToUse/100)):
					trainingDataX.append(data[i][j])
					trainingDataY.append(1)
				if len(self.networks) > 1:
					for j in range(2000):
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
	arr = []
	arr2 = []
	data = []
	for i in range(ord(endLetter) - ord(startLetter) + 1):
		data.append([])
	recording = False

	for (path, dirs, files) in os.walk('./json_output/training'):
		if ord(str(path)[-1]) <= ord(endLetter) and ord(str(path)[-1]) >= ord(startLetter):
			print(str(path))
			for fname in files:
				with open(path + '/' + fname, 'r') as f:
					arr2 = []
					arr = f.read().strip().split('\n')
					for i in range(len(arr)):
						arr[i] = arr[i].split(' ')
						for element in arr[i]:
							if recording:
								try:
									temp = float(str(element).strip())
									if temp > 3:
										arr2.append(temp)
								except:
									if element == 'left:':
										recording = False
							elif element == 'right:':
								recording = True
					for i in range(len(arr2)):
						if arr2[i] > maxMins[i][0]:
							maxMins[i][0] = arr2[i]
						if arr2[i] < maxMins[i][1]:
							maxMins[i][1] = arr2[i]
					data[ord(str(path)[-1]) - ord('A')].append(arr2)
	for i in range(len(data)):
		for j in range(len(data[i])):
			for k in range(len(data[i][j])):
				if maxMins[k][0] == maxMins[k][1]:
					data[i][j][k] = 0.0
				else:
					data[i][j][k] = (data[i][j][k] - maxMins[k][1]) / (maxMins[k][0] - maxMins[k][1])
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
	for i in range(42):
		maxMins.append([0.0, 10000.0])
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
		temp = 0
		for j in range(len(data[i])):
			if g.type == "mono" and g.predict([data[i][j]])[0] == i:
				temp += 1
			elif g.type == "multi" and i in g.predict([data[i][j]]):
				temp += 1
		print(chr(i + ord('A')) + ": " + str(temp/len(data[i])))
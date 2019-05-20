import network as NN
import numpy as np
import pickle
import sys
import os
import random

class Guesser(object):
	def __init__(self, type="multi", name="tempNet"):
		self.networks = []
		self.type = type
		self.name = name
		if type == "multi":
			for i in range(26):
				self.networks.append(NN.Network([63, 63, 1]))
		elif type == "mono":
			self.networks.append(NN.Network([63, 63, 26]))
		else:
			print("Invalid type")
			sys.exit(1)
	
	def train(self):
		data = buildData()
		if self.type == "mono":
			trainingData = []
			iterator = 0
			for i in range(5000):
				r1 = random.randint(0,25)
				r2 = random.randint(0, len(data[r1])-1)
				print("r1:" + str(r1) + " r2:" + str(r2))
				trainingData.append((data[r1][r2],r1))
			self.networks[0].SGD(trainingData, 100, 10, 0.1)
		elif self.type == "multi":
			print("multi training")
			for i in range(26):
				trainingData = []
				for j in range(int(len(data[i])/10)):
					trainingData.append((data[i][j], 1))
				for j in range(2000):
					temp = random.randint(0,25)
					while temp == i:
						temp = random.randint(0,25)
					trainingData.append((data[temp][random.randint(0,len(data[temp])-1)], 0))
				print("Dataset built for " + str(chr(i + ord('A'))))
				self.networks[i].SGD(trainingData, 100, 10, 3)
				print("Finished training " + str(chr(i + ord('A'))))
		else:
			print("Invalid type")
	
	def predict(self, data):
		if self.type == "mono":
			print("Predicting mono")
			for guess in self.networks[0].feedforward(data):
				print(np.argmax(guess))
			print(np.argmax(self.networks[0].feedforward(data)))
		elif self.type == "multi":
			print("Predicting multi")
			highest = 0
			winnerList = []
			for i in range(26):
				value = NN.sigmoid(np.sum(self.networks[i].feedforward(data)*self.networks[i].biases[-1]))
				#print(value)
				if highest < value:
					highest = value
					winnerList.append(i)
			if len(winnerList) < 5:
				for i in winnerList:
					print("Guess is " + str(chr(i + ord('A'))))
			else:
				for i in range(5):
					print("Guess is " + str(chr(winnerList[(i+1)*-1] + ord('A'))))
		else:
			print("Invalid type")

	def save(self):
		pickle.dump(self, open(self.name, "wb"))
	
def buildData():
	arr = []
	arr2 = []
	data = []
	for i in range(26):
		data.append([])
	recording = False

	for (path, dirs, files) in os.walk('./json_output/training'):
		if ord(str(path)[-1]) <= ord('Z') and ord(str(path)[-1]) >= ord('A'):
			print(str(path))
			for fname in files:
				#print(fname)
				with open(path + '/' + fname, 'r') as f:
					arr2 = []
					arr = f.read().strip().split('\n')
					for i in range(len(arr)):
						arr[i] = arr[i].split(' ')
						for element in arr[i]:
							if recording:
								try:
									temp = float(str(element).strip())
									arr2.append(temp)
								except:
									if element == 'left:':
										recording = False
							elif element == 'right:':
								recording = True
					data[ord(str(path)[-1]) - ord('A')].append(np.array(arr2))
	return np.array(data)

if __name__ == "__main__":
	g = pickle.load(open("./monoNet2", "rb"))
	data = buildData()
	g.predict(data[0][0])
import network3 as NN
import numpy as np
import pickle
import sys

class Guesser(object):
	def __init__(self, type="multi", name="tempNet"):
		self.networks = {}
		self.type = type
		self.name = name
		if type == "multi":
			for i in range(26):
				self.networks[str(chr(i + ord('A')))] = NN.Network([63, 63, 1])
		elif type == "mono":
			self.networks["net"] = NN.Network([63, 15, 26])
		else:
			print("Invalid type")
			sys.exit(1)
	
	def train(self, fileName):
		data = buildData(self.type, fileName)
		if self.type == "mono":
			print("mono training")
		elif self.type == "multi":
			print("multi training")
			for i in range(26):
				placement = 0
				trainingData = []
				for item in data:
					if placement == i:
						trainingData.append((item, 1))
					else:
						trainingData.append((item, 0))
					placement += 1
				self.networks[str(chr(i + ord('A')))].SGD(trainingData, 10000, 100, 3)
				print("Finished training " + str(chr(i + ord('A'))))
		else:
			print("Invalid type")
	
	def predict(self, data):
		if self.type == "mono":
			print("Predicting mono")
		elif self.type == "multi":
			print("Predicting multi")
			highest = 0
			winnerList = []
			#print(self.networks['A'].feedforward(data))
			for i in range(26):
				if highest < np.argmax(self.networks[str(chr(i + ord('A')))].feedforward(data)):
					highest = np.argmax(self.networks[str(chr(i + ord('A')))].feedforward(data))
					winnerList.append(i)
			print("Guess is " + str(chr(winnerList[len(winnerList)-1] + ord('A'))))
		else:
			print("Invalid type")

	def save(self):
		pickle.dump(self, open(self.name, "wb"))
	
def buildData(type, fileName):
	if type == "mono":
		print("Build mono data")
	elif type == "multi":
		arr = []
		data = []
		letterCount = 0
		recording = False

		with open(fileName, 'r') as f:
			arr = f.read().strip().split('\n')
			for i in range(len(arr)):
				arr[i] = arr[i].split(' ')
				for element in arr[i]:
					if recording:
						try:
							temp = float(str(element).strip())
							data[letterCount].append(temp)
						except:
							if element == 'left:':
								recording = False
								data[letterCount] = np.array(data[letterCount])
								letterCount += 1
					elif element == 'right:':
						recording = True
						data.append([])
			return np.array(data)

if __name__ == "__main__":
	g = Guesser(type="multi", name="multiNet2")
	g.train('json_info.txt')
	g.save()
	rando = []

	with open('sampleInputA.txt', 'r') as f:
		temp = f.read().strip().split('\n')
		for i in range(len(temp)):
			temp[i] = temp[i].split(' ')
			for j in range(len(temp[i])):
				try:
					num = float(temp[i][j])
					rando.append(num)
				except:
					print('skipping ' + temp[i][j])
	g.predict(rando)
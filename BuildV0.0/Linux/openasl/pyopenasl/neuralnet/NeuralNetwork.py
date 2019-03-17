import numpy as np
import sys

def sigmoid(x):
    return 1.0/(1+ np.exp(-x))

def hyperbolicTan(x):
	return np.tanh(x)

def sigmoid_derivative(x):
    return x * (1.0 - x)

def hyperbolicTan_derivative(x):
	return 1.0 - np.tanh(x)**2

class NeuralNetwork:
	def __init__(self, layers=2, weightLength=2, load=False, name="DaNetwork"):
		self.weights = []
		self.layers = layers
		self.name = name
		if load:
			self.load()
		else:
			self.weights = (2 * np.random.random_sample((layers, weightLength)) - 1) * 0.25


	def train(self, X, y, iterations=10000):
		for i in range(iteration):
			

	def predict(self, x):
		a = np.array(x)
		for l in range(len(self.weights)):
			temp = np.ones(a.shape[0]+1)
			temp[0:-1] = a
			a = hyperbolicTan(np.dot(temp, self.weights[l]))
		return a

	
	def load(self):
		f = open("./" + self.name, "r")
		tempLayers = f.read().split("\n")
		for i in range(len(tempLayers)):
			self.weights.append(tempLayers[i].split(" "))
		self.layers = len(self.weights)
		self.weightLength = len(self.weights[0])


	def save(self):
		output = ""
		for i in range(len(self.weights)):
			for j in range(len(self.weights[i])):
				output += self.weights[i][j]
			if i < len(self.weights) - 1:
				output += "\n"
		f = open("./" + self.name, "w")
		f.write(output)

if __name__ == "__main__":
	X = np.array([[0,0], [0,1], [1,0], [1,1]])
	y = np.array([[0],[1],[1],[0]])
	nn = NeuralNetwork(layers=4)
	nn.train(X, y)
	
	for i in [[0,0], [0,1], [1,0], [1,1]]:
		print(i, nn.predict(i))
	
	nn.save()
	nn = NeuralNetwork(load=True)
	
	for i in [[0,0], [0,1], [1,0], [1,1]]:
		print(i, nn.predict(i))

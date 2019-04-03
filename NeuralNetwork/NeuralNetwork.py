import numpy as np
import random
import pickle
import gzip
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
	def __init__(self, layers=[36,36,26], load=False, name="DaNetwork"):
		self.weights = []
		self.biases = []
		self.layerCount = len(layers)
		self.name = name
		self.activationFunc = sigmoid
		self.activationFuncDir = sigmoid_derivative
		if load:
			self.load()
		else:
			self.biases = [np.random.randn(y, 1) for y in layers[1:]]
			self.weights = [np.random.randn(y, x) for x, y in zip(layers[:-1], layers[1:])]
	
	def feedForward(self, a):
		for b, w in zip(self.biases, self.weights):
			a = self.activationFunc(np.dot(w, a) + b)
		return a
	def backProp(self, x, y):
		tempBias = [np.zeros(b.shape) for b in self.biases]
		tempWeights = [np.zeros(w.shape) for w in self.weights]
		activation = x
		activations = [x]
		zs = []
		for b, w in zip(self.biases, self.weights):
			z = np.dot(w, activation) + b
			zs.append(z)
			activation = self.activationFunc(z)
			activations.append(activation)
		delta = (activations[-1] - y) * self.activationFuncDir(zs[-1])
		tempBias[-1] = delta
		tempWeights[-1] = np.dot(delta, activations[-2].transpose())
		for i in range(2, self.layerCount):
			z = zs[-i]
			sp = self.activationFuncDir(z)
			delta = np.dot(self.weights[-i + 1].transpose(), delta) * sp
			tempBias[-i] = delta
			tempWeights[-i] = np.dot(delta, activations[-i - 1].transpose())
		return(tempBias, tempWeights)
	def train(self, X, y, iterations=10000, batchSize=10, learningRate=3.0):
		data = list(zip(X,y))
		n = len(data)
		for i in range(iterations):
			random.shuffle(data)
			batches = [data[k:k+batchSize] for k in range(0, n, batchSize)]
			for batch in batches:
				tempBias = [np.zeros(b.shape) for b in self.biases]
				tempWeights = [np.zeros(w.shape) for w in self.weights]
				for x, y in batch:
					deltatempBias, deltatempWeights = self.backProp(x, y)
					tempBias = [nb + dnb for nb, dnb in zip(tempBias, deltatempBias)]
					tempWeights = [nw + dnw for nw, dnw in zip(tempWeights, deltatempWeights)]
				self.weights = [w - (learningRate/len(batch)) * nw for w, nw in zip(self.weights, tempWeights)]
				self.biases = [b - (learningRate/len(batch)) * nb for b, nb in zip(self.biases, tempBias)]
			if i % 200 == 0:
				print(str(i) + " iterations complete")

	def predict(self, test_data):
		#test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
		#return sum(int(x == y) for (x, y) in test_results)
		print(self.weights)
		return self.feedForward(test_data)
	
	def load(self):
		f = gzip.open("./" + self.name + ".pkl.gz", "rb")
		self.weights, self.biases = pickle.load(f)
		f.close()
	def save(self):
		f = gzip.open("./" + self.name + ".pkl.gz", "w")
		pickle.dump((self.weights, self.biases), f)
		f.close()

if __name__ == "__main__":
	X = np.array([[0,0], [0,1], [1,0], [1,1]])
	y = np.array([[0],[1],[1],[0]])
	nn = NeuralNetwork(layers=[2,2,1])
	nn.train(X, y, batchSize=1)
	
	for i in [[0,0], [0,1], [1,0], [1,1]]:
		print(i, nn.predict(i))
	
	nn.save()
	nn = NeuralNetwork(load=True)
	
	for i in [[0,0], [0,1], [1,0], [1,1]]:
		print(i, nn.predict([i]))
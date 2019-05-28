from skimage.io import imread
from skimage.color import rgb2gray
from skimage.feature import *
from sklearn.neural_network import MLPClassifier as NN
import pickle
import sys
import os
import random

nets = []
data = [[], [], [], [], []]
X = []
Y = []

for i in range(5):
	nets.append(NN(hidden_layer_sizes=(100, 100), activation="tanh", solver="adam", max_iter=500))

for path, dirs, files in os.walk("./Cropped"):
	if ord(path[-1]) >= ord('A') and ord(path[-1]) <= ord('E'):
		for f in files:
			data[ord(path[-1])-ord('A')].append(hog(rgb2gray(imread(path + "/" + f)), feature_vector=True))

print(len(data))
print(len(nets))

for i in range(len(nets)):
	print("Training " + str(i))
	del X[:]
	del Y[:]
	for j in range(len(data)):
		if j == i:
			X.append(data[i][j])
			Y.append(1)
		else:
			X.append(data[i][j])
			Y.append(0)
	nets[i].fit(X, Y)

for i in range(len(nets)):
	pickle.dump(nets[i], open("net" + str(i), "wb"))

for i in range(len(nets)):
	a = 0
	t = 0
	for j in range(len(data)):
		for k in range(len(data[j])):
			p = nets[i].predict([data[j][k]])[0]
			if i == j and p == 1:
				a += 1
			elif p == 0:
				a += 1
			t += 1
	print("Accuracy: " + str(float(a)/float(t)))
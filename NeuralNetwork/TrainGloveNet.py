import numpy as np
from skimage.io import imread
from skimage.segmentation import slic
from sklearn.neural_network import MLPClassifier as NN
import random
import pickle

img = imread("./A2.jpg")
labels = slic(img, n_segments=100, compactness=20)
net = NN(hidden_layer_sizes=(10,10), activation="tanh", solver="adam", max_iter=500)

hits = [55]
X = []
Y = []

yes = 0

for i in range(len(labels)):
	for j in range(len(labels)):
		if labels[i][j] in hits:
			X.append(np.array(img[i][j]))
			Y.append(1)
			yes += 1
		elif random.randint(1, 5) == 3:
			X.append(np.array(img[i][j]))
			Y.append(0)

print("Training")
print("Positive ratio: " + str(float(float(yes)/float(len(X))) * 100))

net.fit(X,Y)
pickle.dump(net, open("gloveNet6", "wb"))
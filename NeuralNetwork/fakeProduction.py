from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.feature import *
from sklearn.neural_network import MLPClassifier as NN
from multiNetPictureProcess import *
from BlobFinder import *
from letterGuesser3 import *
import numpy as np
import pickle
import sys
import os

letters = []
shapeM = np.array([[[0,0,1]]*50]*50)

for path, dirs, files in os.walk("."):
	del dirs[:]
	for fname in files:
		if fname[-3:] == "jpg" and "blacked" not in fname and "cropped" not in fname:
			
			if (isolateHand(fname[:-4], ".", ".") == 1):
				print("Error isolating images, exiting")
				exit()
			print("Waiting for threads to complete")
			for t in threads:
				while t.is_alive():
					pass
			print("Threads complete")
			del threads[:]
			del nets[:]
			del imgs[:]
			CropHand(fname[:-4], ".", ".")
			
			img = canny(rgb2gray(imread(fname[:-4] + "cropped.jpg")))
			cimg = imread(fname[:-4] + "cropped.jpg")
			Axx, Axy, Ayy = structure_tensor(rgb2gray(imread(fname[:-4] + "cropped.jpg")), sigma=0.1)
			img2D = structure_tensor_eigvals(Axx, Axy, Ayy)[0]
			img1D = []
			img1D2 = []
			bb = cimg*shapeM
			bbMax = np.amax(bb)
			bb = bb / np.array([[[1,1,float(bbMax)]]*50]*50)
			bb = bb.flatten()[2::3]
			for obj in img2D:
				for el in obj:
					img1D2.append(el)
			for i in range(len(img)):
				for j in range(len(img[i])):
					img1D.append(img[i][j])
			letters.append([[img1D], [img1D2], [hog(rgb2gray(imread(fname[:-4] + "cropped.jpg")))], [bb], fname[0]])
xcannyNet = pickle.load(open("xcannyNet", "rb"))
hogNet = pickle.load(open("hogNet", "rb"))
tensorNet = pickle.load(open("tensorNet", "rb"))
blueBoostNet = pickle.load(open("blueBoostNet", "rb"))

for i in range(len(letters)):
	letters[i].append(xcannyNet.predict(letters[i][0]))
	letters[i].append(tensorNet.predict(letters[i][1]))
	letters[i].append(hogNet.predict(letters[i][2]))
	letters[i].append(blueBoostNet.predict(letters[i][3]))
	print(letters[i][4])
	print("xcannyNet: " + str(letters[i][5]))
	print("hogNet: " + str(letters[i][6]))
	print("tensorNet: " + str(letters[i][7]))
	print("blueBoostNet: " + str(letters[i][8]))
	print("\n")
from skimage.io import imread, imsave
from skimage.feature import blob_log
from skimage.color import rgba2rgb
from sklearn.neural_network import MLPClassifier as NN
import numpy as np
import pickle
import threading
import os

nets = []
imgs = []
threads = []

def predict(index, name, img):
	#print(len(img))
	#print(len(img[0]))
	for i in range(len(img)):
		for j in range(len(img[i])):
			prediction = nets[index].predict([img[i][j]])
			if prediction[0] == 1:
				imgs[index][0][i][j] = img[i][j]
				imgs[index][1] += 1
			else:
				imgs[index][0][i][j] = [0, 0, 0]
	print(name + " complete")

def isolateHand(iname, sourcedir, targetdir):
	#print(os.getcwd())
	img = rgba2rgb(imread(sourcedir + "/" + iname + ".jpg"))
	netNames = ["gloveNet", "gloveNet2", "gloveNet3", "gloveNet4", "gloveNet5", "gloveNet6"]

	print("Setting up environment")
	for i in range(len(netNames)):
		timg = []
		for obj in img:
			timg.append(np.array(obj))
		timg = np.array(timg)
		imgs.append([timg, 0])
		
		nets.append(pickle.load(open("./NeuralNetwork/" + netNames[i], "rb")))
		
		threads.append(threading.Thread(target=predict, args=(i, "Thread" + str(i), img)))

	print("Launching threads")
	for i in range(len(threads)):
		threads[i].start()
		print("Thread" + str(i) + " away!")
	print("Joining threads")
	for i in range(len(threads)):
		threads[i].join()

	print("Picking best option")
	best = -1
	brightest = -1
	num = len(img) * len(img[0])
	num2 = 0
	threshold = int(num * 0.025)
	for i in range(len(imgs)):
		if imgs[i][1] > threshold and imgs[i][1] < num:
			best = i
			num = imgs[i][1]
		if imgs[i][1] > threshold and imgs[i][1] > num2:
			brightest = i
			num2 = imgs[i][1]
	
	if best == -1:
		print("Error with selection process")
		print(len(img))
		print(len(img[0]))
		print(len(imgs))
		return 1
	else:
		"""
		blobs = blob_log(imgs[best][0])
		x = 0
		y = 0
		r = 0
		for obj in blobs:
			if obj[-1] > r:
				x = int(obj[0])
				y = int(obj[1])
				r = int(obj[-1])
		r = int(r*2)
		for i in range((x-r), (x+r)):
			for j in range((y-r), (y+r)):
				if (imgs[best][0][i][j][0] == 0 and imgs[best][0][i][j][1] == 0 and imgs[best][0][i][j][2] == 0):
					imgs[best][0][i][j] = imgs[brightest][0][i][j]
		"""
		print("Chosen network: " + netNames[best])
		imsave(targetdir + "/" + iname + "blacked.jpg", imgs[best][0])
		return 0
if __name__ == "__main__":
	print("Whoops")
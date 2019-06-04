from skimage.io import imread, imsave
from skimage.color import rgba2rgb
from skimage.segmentation import slic
import numpy as np

img = rgba2rgb(imread("./tempImage0.jpg"))
labels = slic(img, n_segments=100, compactness=20)

timg = []

for obj in img:
	timg.append(np.array(obj))
timg = np.array(timg)

max = 0

for i in range(len(labels)):
	for j in range(len(labels[i])):
		if max < labels[i][j]:
			max = labels[i][j]

for x in range(max):
	for i in range(len(labels)):
		for j in range(len(labels[i])):
			if labels[i][j] == x:
				timg[i][j] = img[i][j]
			else:
				timg[i][j] = [0,0,0]
	imsave("./DemoSegments/" + str(x) + ".jpg", timg)
from skimage import data, feature, exposure
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage.color import rgb2gray
import numpy as np

def CropHand(iname, sourcedir, targetdir):
	img = imread(sourcedir + "/" + iname + "blacked.jpg")
	blobs = feature.blob_log(img)
	x = 0
	y = 0
	r = 0

	for obj in blobs:
		if obj[-1] > r:
			x = int(obj[0])
			y = int(obj[1])
			r = int(obj[-1])
	r = int(r*2)
	cropped = resize(img[(x - r):(x + r), (y - r):(y + r)], (50, 50))

	imsave(targetdir + "/" + iname + "cropped.jpg", cropped)
from skimage.io import imread, imsave
from skimage.feature import blob_log
import numpy as np
import os

"""
shapeM = np.array([[[0,0,1]]*352]*288)
maxM = np.array([[[0,0,float(255)]]*352]*288)
"""

shapeM = np.array([[[0,0,1]]*50]*50)
maxM = np.array([[[0,0,float(255)]]*50]*50)

for path, dirs, files in os.walk("./Cropped"):
	if ord(path[-1]) >= ord('A') and ord(path[-1]) <= ord('Z'):
		for fname in files:
			img = imread(path + "/" + fname)
			max = np.amax(img*shapeM)
			grayed = np.array([[[1,1,1]]*50]*50)
			blued = img*shapeM
			blued = blued/np.array([[[1,1,float(max)]]*50]*50)*maxM
			blued = np.array(blued, np.int32)
			grayed = grayed * blued.flatten()[2::3].reshape((50,50,1))
			imsave("./BlueBoost/" + path[-1] + "/" + fname, blued)
			imsave("./GrayedBlueBoost/" + path[-1] + "/" + fname, grayed)
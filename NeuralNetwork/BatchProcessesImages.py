from multiNetPictureProcess import *
from BlobFinder import *
import sys
import os

for path, dirs, files in os.walk("."):
	del dirs[:]
	for f in files:
		if f[-3:] == "jpg":
			print("Working on " + f[:-4])
			if (isolateHand(f[:-4], ".", "./BlueHandAlphabet/Blacked/" + f[0]) == 1):
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
			CropHand(f[:-4], "./BlueHandAlphabet/Blacked/" + f[0], "./BlueHandAlphabet/Cropped/" + f[0])
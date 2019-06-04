from .multiNetPictureProcess import *
from .BlobFinder import *
import sys
import os

def blackAndCrop():
	print("Processing")
	for path, dirs, files in os.walk("./NeuralNetwork/BlueHandAlphabet/Images"):
		#print(files)
		#print(dirs)
		for f in files:
			if f[-3:] == "jpg":
				print("Working on " + f[:-4])
				if (isolateHand(f[:-4], "./NeuralNetwork/BlueHandAlphabet/Images/" + f[0], "./NeuralNetwork/BlueHandAlphabet/Blacked/" + f[0]) == 1):
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
				CropHand(f[:-4], "./NeuralNetwork/BlueHandAlphabet/Blacked/" + f[0], "./NeuralNetwork/BlueHandAlphabet/Cropped/" + f[0])
if __name__ == "__main__":
	blackAndCrop()
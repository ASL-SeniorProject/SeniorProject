import os, sys
import errno

from pathlib import Path

import json

cwd = os.getcwd()

ASL_IMAGES = "/images/asl_images/"

TRAINING = cwd + ASL_IMAGES + "asl_alphabet_train/"
TESTING = ASL_IMAGES + "asl_alphabet_test/"

OUTPUT = cwd + "/json_output/"

TRAIN_OUT = OUTPUT + "training/"
TEST_OUT = OUTPUT + "testing/"

from OpenPoseExe import Command

class FileIO(object):

	def __init__(self, input_dir=None, output_dir=None):
		self.input_dir = input_dir
		self.output_dir = output_dir

	# reads a directory and returns a list of filenames
	def read_image_strings(self, path=None):
		imgs = []
		if path is None and self.input_dir is not None:
			path = self.input_dir

		for root, dirs, files in os.walk(path):
			for filename in files:
				imgs.append(filename)
		return imgs

	def read_letter_data(self, letter=''):
		files = self.read_image_strings(letter)
		print(files)

	def read_video_to_json(self, file_path):
		pass

class OpenPoseIO(object):
	def __init__(self):
		self.f_io = FileIO(ASL_IMAGES)
		self.cmd = Command()

	# populate training data
	def populate_training_data(self):
		"""for root, dirs, filenames in os.walk(TRAINING):
			for d in dirs:
				letter_in = TRAINING + str(d) + "/"
				letter_out = TRAIN_OUT + str(d) + "/"
				try:
					if not os.path.isdir(letter_out):
						os.mkdir(letter_out)
				except OSError as e:
					pass"""

		self.cmd.image_to_json(img_path=TESTING, img_out=TEST_OUT)
	# populate testing data 
	#    get image string list in directory
	#    get size of list
	#    pop off 1/4 values
	#    this is test images for one letter
if __name__ == "__main__":
	openpose_io = OpenPoseIO()
	openpose_io.populate_training_data()

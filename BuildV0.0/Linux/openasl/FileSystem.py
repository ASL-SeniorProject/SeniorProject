import os, sys

parent = "../" + os.getcwd()
cwd = os.getcwd()

class FileIO(object):

	def __init__(self, input_dir=None, output_dir=None):
		self.input_dir = input_dir
		self.output_dir = output_dir

	# reads an input image, runs OpenPose, outputs JSON to output_dir
	def read_image_strings(self, path=None):
		imgs = []
		if path is None and self.input_dir is not None:
			path = self.input_dir

		print(path)

		for root, dirs, files in os.walk(cwd + path):
			for filename in files:
				imgs.append(filename)
		return imgs

	def read_video_to_json(self, file_path):
		pass


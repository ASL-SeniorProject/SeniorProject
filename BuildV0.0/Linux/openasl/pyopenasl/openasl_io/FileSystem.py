import os, sys

from pathlib import Path

import json
import simplejson

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

		for root, dirs, files in os.walk(cwd + path):
			for filename in files:
				imgs.append(filename)
		return imgs

	# goes into json directory and reads
	def read_json_as_list(self, path=None):
		if path is None:
			path = str(Path(cwd).parent) + "/openasl/json_output/"

		print(path)
		json_data = []
		for root, dirs, files in os.walk(path):
			print(root)
			for f in files:
				f_r = open(path + f, "r")
				j_data = f_r.read()
				#j_data = json.loads(path + f)
				json_data.append(j_data)

		return json_data

	def read_video_to_json(self, file_path):
		pass


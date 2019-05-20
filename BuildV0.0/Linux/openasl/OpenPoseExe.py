import os, sys

#from FileSystem import FileIO
#from pyopenasl import openasl_io as asl_io
from pyopenasl import neuralnet as nn

#fs = asl_io.FileSystem

parent = "/../"
		
cmd = "./"
#openpose_dir = "/../openpose/"
openpose_dir = "openpose/"
openasl_dir = "openasl/"

openpose_exe = cmd + "build/examples/tutorial_api_cpp/07_hand_from_image.bin"

JSON_OUT = "/json_output/"

ASL_IMGS = "~/Desktop/asl_images" 

INITIAL_SET = "/images/initial_set/"

class Command(object):

	# can be init'd with a command at creation
	def __init__(self, cmd=None, *opts):
		self.cmd = cmd
		self.options = opts

	# get json from img at img_path and output to img_out
	def image_to_json(self, img_path, img_out, option="", view=None):
		args = [img_path, img_out]
		self.options = args
		self.run(openpose_exe, args)
		
	# execute the command
	def run(self, cmd=None, *opts):
		c = opts
		for cc in c:
			cmd = cmd + " " + str(cc)

		os.chdir("..")
		os.chdir(openpose_dir)
		os.system(cmd)
		#os.chdir("..")
		#os.chdir(openasl_dir)


"""if __name__ == "__main__":
	f_io = FileIO("./images/initial_set/", ".")
	imgs = f_io.read_image_strings("./images/initial_set/")
	
	img = imgs[0]
	cmd = Command()
	cmd.image_to_json(img_path=img, view="--view", img_out=".")

	json_data = f_io.read_json_as_list()"""

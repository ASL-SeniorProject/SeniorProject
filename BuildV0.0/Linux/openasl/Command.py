import os, sys

from FileSystem import FileIO

parent = "/../"
		
cmd = "./"
#openpose_dir = "/../openpose/"
openpose_dir = "openpose/"
openpose_exe = cmd + "build/examples/openpose/openpose.bin"

hand = "--hand"
face = "--face"

image = "--image_dir"
video = "--video"

json = "--write_json"

#JSON_OUT = "../json_output/"
JSON_OUT = "/json_output/"


HAND_IMG = "single"
HAND_VIDEO = "video"

#IMG_PATH = "../images/tmp/"
IMG_PATH = "/images/tmp/"

INITIAL_SET = "/images/initial_set/"

class Command(object):

	# can be init'd with a command at creation
	def __init__(self, cmd=None, *opts):
		self.cmd = cmd
		self.options = opts

	# get json from img at img_path and output to img_out
	def image_to_json(self, img_path, img_out, option=HAND_IMG, view=None):
		args = []
		if option == HAND_IMG:
			#args = [image, str(os.getcwd() + IMG_PATH), json, str(os.getcwd() + JSON_OUT), hand, "--display 0", "--render_pose 0"]	
			args = [image, str(os.getcwd() + INITIAL_SET), json, str(os.getcwd() + JSON_OUT), hand, "--hand_detector 2 --hand_scale_number 6 --hand_scale_range 0.4"]	
			

		self.run(openpose_exe, "--view", args)
		
	# execute the command
	def run(self, cmd=None, view=None, *opts):
		if cmd is not None and opts is not None:
			self.cmd = cmd
			self.options = opts

		c = opts[0]
		for cc in c:
			cmd = cmd + " " + str(cc)

		if view == "--view":
			print(cmd)

		os.chdir("..")
#		os.chdir("..")
		os.chdir(openpose_dir)
		os.system(cmd)
		os.chdir("..")
#		os.chdir("..")
		#os.chdir("openasl/pyopenasl")
		os.chdir("openasl/")


if __name__ == "__main__":
	f_io = FileIO(IMG_PATH, ".")
	imgs = f_io.read_image_strings()

	img = imgs[0]
	cmd = Command()
	cmd.image_to_json(img_path=img, view="--view", img_out=".")

	json_data = f_io.read_json_as_list()
		

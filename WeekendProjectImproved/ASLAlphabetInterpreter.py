from sklearn.svm import SVC

class ASLAlphabetInterpreter(object):
	def __init__(self):
		self.workingDir = ""
		self.handFinder = None
		self.translater = None
		self.lettersList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N',
	   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

	def train(self, set):
		for s in set:
			
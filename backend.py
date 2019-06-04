from flask import Flask
from binascii import a2b_base64
from flask_cors import CORS
from flask import request
from flask import jsonify
from NeuralNetwork.BatchProcessesImages import *
from NeuralNetwork.BlobFinder import *
from NeuralNetwork.letterGuesser3 import * 
from NeuralNetwork.multiNetPictureProcess import *
from NeuralNetwork.TrainGloveNet import *
from NeuralNetwork.fakeProduction import *
from subprocess import Popen, check_output
import string
import math
import json
app = Flask(__name__)
CORS(app)

# The global translation of the message so far
global message
message = ''

global numCalibrated
numCalibrated = 0

global collection
collection = []

letters = list(string.ascii_uppercase[:26])

# GET method for retrieving the current message
@app.route('/')
def read_message():
    return message

# GET request for adding a letter to the current message
@app.route('/addLetter/<letter>')
def add_letter(letter):
    global message
    message = message + letter
    return message

# GET request for clearing the current message
@app.route('/clearMessage/')
def clear_message():
    global message
    message = ''
    return message	

@app.route('/calibrate', methods = ['POST'])
def calibrate():
	"""
	jsonData=request.get_json()
	data = jsonData['image']
	binary_data = a2b_base64(data)
	
	global numCalibrated
	fd = open(letters[int(math.floor(numCalibrated / 20))] + str(numCalibrated % 20) + ".jpg", 'wb')
	numCalibrated += 1

	fd.write(binary_data)
	fd.close()
	"""
	blackAndCrop()
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# POST request used by the front end to send an image to the server
@app.route('/processImage', methods = ['POST'])
def process_image():
    jsonData = request.get_json()
    data = jsonData['image']
    binary_data = a2b_base64(data)
    global numCalibrated
    fd = open('tempImage' + str(numCalibrated) + '.jpg', 'wb')
    numCalibrated += 1
    fd.write(binary_data)
    fd.close()
    #Call predict letter
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def makeWords(wSoFar, letters):
    if len(letters) == 0:
        global collection
        collection.append(wSoFar)
        return
    for c in letters[0]:
        makeWords(wSoFar + chr(ord('A') + c), letters[1:])
@app.route('/predict')
def predictLetter():
	guessedLetters = processAndPredict()
	makeWords('', guessedLetters)
	global collection
	global message
	message = ''
	endWord = []
	for w in collection:
		#words = str(check_output(['java', '-jar',  'Checker-1.0-SNAPSHOT-jar-with-dependencies.jar', w])).split('{')[1:]
		message = str(check_output(['java', '-jar',  'Checker-1.0-SNAPSHOT-jar-with-dependencies.jar', w]))
		#message = str(words)
		"""
		words = words[0].split('}')[0].split(' ')
		if words[0][-1] == ',':
			endWord.append(words[0][:-1])
		else:
			endWord.append(words[0])
		"""	
	#message = endWord[0]
	p = Popen("clean.bat", cwd=r""+os.getcwd())
if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=5000)

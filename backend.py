from flask import Flask
from binascii import a2b_base64
from flask_cors import CORS
from flask import request
import string
import math
app = Flask(__name__)
CORS(app)

# The global translation of the message so far
global message
message = ''

global numCalibrated
numCalibrated = 0

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
	jsonData=request.get_json()
	data = jsonData['image']
	binary_data = a2b_base64(data)
	
	global numCalibrated
	fd = open(letters[int(math.floor(numCalibrated / 20))] + str(numCalibrated % 20) + ".jpg", 'wb')
	numCalibrated += 1

	fd.write(binary_data)
	fd.close()
	return "GOOD"
	
	

# POST request used by the front end to send an image to the server
@app.route('/processImage', methods = ['POST'])
def process_image():
    jsonData = request.get_json()
    data = jsonData['image']
    binary_data = a2b_base64(data)

    fd = open('image.jpg', 'wb')
    fd.write(binary_data)
    fd.close()
    
	#Call predict letter
	#predictLetter()
    return "SUCCESS"

def predictLetter():
	print("Call Nick's nueral net")
	print("Add its prediction")
	print("Process all output with NLP")
	print("Update message with the new outpu")

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=5010)

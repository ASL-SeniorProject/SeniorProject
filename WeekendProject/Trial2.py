from gesture_recognizer1 import *
from skimage import io

print("Creating temporary model")
tinterpreter = GestureRecognizer()
print("Opening previous model")
interpreter = tinterpreter.load_model("babyReader")
print("Running predication")
pos, pred = interpreter.recognize_gesture(io.imread("./Dataset/user_3/A0.jpg"))

print(pos)
print(pred)
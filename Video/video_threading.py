from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from PIL import Image
import numpy as np
import pytesseract
import argparse
import imutils
import json
import time
import cv2
import os


def getFeatureMap(image):
	meanHue = cv2.mean(hue)
	meanHue = meanHue[0]	
	stdDev = np.std(hue)
	
	_, notMean1 = cv2.threshold(hue, meanHue + 2*stdDev, 255, cv2.THRESH_BINARY)
	_, notMean2 = cv2.threshold(hue, meanHue - 2*stdDev, 255, cv2.THRESH_BINARY_INV)
	notMean = notMean1 + notMean2
	return notMean


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="1 - display, 0 - don't display")
args = vars(ap.parse_args())

vs = PiVideoStream(resolution=(640, 480)).start()
time.sleep(2.0)
fps = FPS().start()
count = 0
disp = False
if args["display"] > 0:
	disp = True

while 1:
	frame = vs.read()
	
	frameBlur = cv2.blur(frame, (5, 5))
	hsvFrame = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2HSV)
	hue, sat, val = cv2.split(hsvFrame)
	
	notMean = getFeatureMap(hue)
	
	connectivity = 8
	ccws = cv2.connectedComponentsWithStats(notMean, connectivity, cv2.CV_32S)
	numLabels = ccws[0]
	labels = ccws[1]
	stats = ccws[2]
	centroids = ccws[3]
	maxInd = numLabels
	
	sortIdx = stats[:, 3].argsort()[::-1]
	sortedStats = stats[sortIdx]
	sortedCentroids = centroids[sortIdx]	
	# Remove all components less thn 28 * 28 which is the size of the pictures
	# in the MNIST dataset. Consider that as minimum for character recognition
	areaIdx = sortedStats[:, cv2.CC_STAT_AREA] > 784
	sortedStats = sortedStats[areaIdx, :]
	sortedCentroids = sortedCentroids[areaIdx, :]
	numLabels = len(sortedStats)
	
	rects = []
	centers = []
	#print(sortedStats[:, cv2.CC_STAT_AREA])
	for i in range(1, numLabels):
		rect = (sortedStats[i, cv2.CC_STAT_LEFT],
		        sortedStats[i, cv2.CC_STAT_TOP],
		        sortedStats[i, cv2.CC_STAT_LEFT] + sortedStats[i, cv2.CC_STAT_WIDTH],
		        sortedStats[i, cv2.CC_STAT_TOP] + sortedStats[i, cv2.CC_STAT_HEIGHT])
		center = (int(sortedCentroids[i, 0]), int(sortedCentroids[i, 1]))
		rects.append(rect)
		centers.append(center)
		#filename = "temp.png"
		#cv2.imwrite(filename, frame[rect[0]:rect[2], rect[1]:rect[3]])
		#text = pytesseract.image_to_string(Image.open('temp.png'))
		#print(text)
		#os.remove(filename)
		cv2.putText(frame, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
		cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 2)	
	
	if disp:
		cv2.imshow("Frame", frame)
		#cv2.imwrite("frame.png", frame) 
	
	fps.update()
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord('q'):
		break
	
	if count % 30 == 0:
		fps.stop()
		#print("FPS: {:.2f}\r".format(fps.fps()), end="", flush=True)
		fps = FPS().start()
		#dict = {'type':'standard', 'latitude':39.2292, 'longitude':-75.9393,
		#	'orientation':'n', 'shape':'star', 'background_color':'orange',
		#	'alphanumeric':'C', 'alphanumeric_color':'black'}
		#jsonDict = json.dumps(dict)
		#with open('data.json', 'w') as outfile:
		#	json.dump(dict, outfile)
								
	count = count + 1

cv2.destroyAllWindows()
vs.stop()



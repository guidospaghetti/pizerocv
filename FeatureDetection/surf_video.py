# import the necessary packages
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import signal
import sys
import imutils
import time
import cv2

def signal_handler(signal, frame):
	vs.stop()
	fps.stop()
	cv2.destroyAllWindows()

signal.signal(signal.SIGINT, signal_handler)
global vs = PiVideoStream(resolution=(640, 480)).start()

# initiate the FAST detector
surf = cv2.xfeatures2d.SURF_create()

# allow time for the camera to warm up
time.sleep(2.0)

global fps = FPS().start()
count = 0

while 1:
	frame = vs.read()
	kp = surf.detect(frame, None)
	img2 = cv2.drawKeypoints(frame, kp, frame, color=(255, 0, 0))
	
	# cv2.imshow("Image", img2)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

	fps.update()
	if count % 30 == 0:
		fps.stop()
		print("FPS: {:.2f}".format(fps.fps()))
		fps.start()

vs.stop()
fps.stop()
cv2.destroyAllWindows()    

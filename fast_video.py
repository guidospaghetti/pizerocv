# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size = (640, 480))

# initiate the FAST detector
fast = cv2.FastFeatureDetector_create()

# allow time for the camera to warm up
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	kp = fast.detect(image, None)
	img2 = cv2.drawKeypoints(image, kp, image, color=(255, 0, 0))
	
	cv2.imshow("Image", img2)
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	if key == ord("q"):
		break
    

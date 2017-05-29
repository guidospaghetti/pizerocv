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

# initiate the ORB detector
orb = cv2.ORB_create()

# allow time for the camera to warm up
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupted/unoccupied text
	image = frame.array
	
	# find keypoints
	kp = orb.detect(image, None)
	
	# compute the descriptors
	kp, des = orb.compute(image, kp)
	
	# draw the keypoints
	img2 = cv2.drawKeypoints(image, kp, image, color = (0, 255, 0), flags=0)
	cv2.imshow("Frame", img2)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the q key was pressed, break the loop
	if key == ord("q"):
		break


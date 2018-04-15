# Import the necessary packages
from imutils.video.pivideostream import PiVideoStream
import argparse
import datetime
import imutils
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-s", "--save-video", help="path to folder to save video")
args = vars(ap.parse_args())

# If the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = PiVideoStream(resolution=(640, 480)).start()
	time.sleep(2.0)

# Otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# If the save video argument is None, save to current folder
if args.get("save_video", None) is None:
	path = ""
else:
	path = args.get("save_video", None)

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(path + "output.avi", fourcc, 20.0, (500, 375))

# Initialize the first frame in the video stream
firstFrame = None

# Loop over the frames of the video
try:
	while True:
		
		# Grab the current frame and initialize the occupied/unoccupied text
		frame = camera.read()
		text = "Unoccupied"
		
		# If the frame is None, then we have reached the end of the video
		if frame is None:
			break

		# Resize the frame and convert it to grayscale, and blur it
		frame = imutils.resize(frame, width = 500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		# If the first frame is None then initialize it
		if firstFrame is None:
			firstFrame = gray
			continue

		# Compute the absolute difference between the current frame and the first frame
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		
		# Dilate the thresholded image to fill in holes, then find contours on the
		# thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for c in contours:
			# If the contour is too small, ignore it
			if cv2.contourArea(c) < args["min_area"]:
				continue
			
			# Computre the bounding box of the contour, draw it, and update the test
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
			text = "Occupied"
			
		# Draw the text and timestamp on the frame
		cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
			 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# Show the frames (slow)
		# cv2.imshow("Security Feed", frame)
		# cv2.imshow("Thresholded Image", thresh)
		# cv2.imshow("Frame Delta", frameDelta)
		# key = cv2.waitKey(1) & 0xFF
		
		# cv2.imwrite("frame.png", frame)
		# cv2.imwrite("thresh.png", thresh)
		# cv2.imwrite("delta.png", frameDelta)	
		
		out.write(frame)

		# If the 'q' key is pressed, break the loop
		# if key == ord('q'):
	 	# break

except KeyboardInterrupt:
	print("Interrupted!")

try:
	camera.stop()
except:
	camera.release()
out.release()
cv2.destroyAllWindows()

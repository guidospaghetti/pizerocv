from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import cv2

vs = PiVideoStream(resolution=(640, 480)).start()
time.sleep(2.0)

while 1:
	frame = vs.read()
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break

cv2.destroyAllWindows()
vs.stop()



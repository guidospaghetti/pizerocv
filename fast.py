import cv2
import numpy as np

img = cv2.imread('roi.jpg', 0)

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector_create()

# Find and draw the keypoints
kp = fast.detect(img, None)
img2 = cv2.drawKeypoints(img, kp, img, color=(255, 0, 0))

cv2.imshow('Image', img2)
cv2.waitKey(0)



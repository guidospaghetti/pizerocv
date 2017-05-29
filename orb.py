import cv2
import numpy as np

img = cv2.imread('roi.jpg', 0)

# Initiate ORB detector
orb = cv2.ORB_create()

# Find the keypoints with ORB
kp = orb.detect(img, None)

# Compute the descriptors with ORB
kp, des = orb.compute(img, kp)

# Draw only keypoints location, not size and orientation
img2 = cv2.drawKeypoints(img, kp, img, color=(0, 255, 0), flags=0)
cv2.imshow('Image', img2)
cv2.waitKey(0)


from skimage import data
from scipy import ndimage
import cv2
import numpy as np

##################################
## assessing max or min value:	##
## np.max(dilation)		##

img = cv2.imread('mask.ctrl.3.jpg', cv2.IMREAD_GRAYSCALE)
height, width = img.shape[:2]

kernel = np.ones((51,51),np.uint8) # How many pixel of extension do I get
dilation = cv2.dilate(img,kernel,iterations = 1) # What does iteration do?

dilation  = np.where(dilation == 255, 127, dilation) 		## WHT to GRY
remake    = np.where(dilation != 127, 0, dilation)		## Smoothing
remake    = np.where(img > 127, 200, dilation)			## mark the tumor inside light GRY
## remake    = np.where(img > 127, 0, dilation) # creates a gray ring surrounding the black FG
remake    = np.where(remake < 127, 0, remake)			## Embelishment
remake    = np.where(remake > 200, 0, remake)			## Embelishment
remake    = np.where(remake == 200, 255, remake)		## light GRY to WHT

cv2.imwrite('ctrl_trimap.png', remake)
# cv2.imwrite('example.png', remake)
# cv2.imwrite('example.bmp', remake)
# print(np.max(remake))


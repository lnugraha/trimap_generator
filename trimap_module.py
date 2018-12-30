import cv2, os
import numpy as np

def trimap_generate(image, name, size, number):
    """
    This function creates a trimap based on simple dilation algorithm
    Inputs [3]: a binary image (black & white only), name of the image, dilation pixels 
    Output    : a trimap
    """
    pixels    = 2*size + 1;                                     # double and plus 1 to have an odd-sized kernel            
    kernel    = np.ones((pixels,pixels),np.uint8)               # How many pixel of extension do I get
    dilation  = cv2.dilate(image, kernel, iterations = 1)

    dilation  = np.where(dilation == 255, 127, dilation) 	## WHITE to GRAY
    remake    = np.where(dilation != 127, 0, dilation)		## Smoothing
    remake    = np.where(image > 127, 200, dilation)		## mark the tumor inside GRAY

    remake    = np.where(remake < 127, 0, remake)		## Embelishment
    remake    = np.where(remake > 200, 0, remake)		## Embelishment
    remake    = np.where(remake == 200, 255, remake)		## GRAY to WHITE

    path = "./images/results/"                                  ## Change the directory
    new_name = '{}px_'.format(size) + name + '_{}.png'.format(number);
    cv2.imwrite(os.path.join(path , new_name) , remake)

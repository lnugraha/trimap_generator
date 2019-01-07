import cv2, os
import numpy as np

def trimap_generate(image, name, size, number, erosion=False):
    """
    This function creates a trimap based on simple dilation algorithm
    Inputs [4]: a binary image (black & white only), name of the image, dilation pixels 
                the last argument is optional; i.e., how many iterations will the image get eroded                 
    Output    : a trimap
    """
    pixels    = 2*size + 1;                                     ## Double and plus 1 to have an odd-sized kernel            
    kernel    = np.ones((pixels,pixels),np.uint8)               ## How many pixel of extension do I get

    if erosion is not False:
        erosion = int(erosion)                                    
        erosion_kernel = np.ones((3,3), np.uint8)                 ## Design an odd-sized erosion kernel
        img = cv2.erode(img, erosion_kernel, iterations=erosion)  ## How many erosion do you expect
        img = np.where(img > 0, 255, img)                         ## Any gray-clored pixel becomes white (smoothing)

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

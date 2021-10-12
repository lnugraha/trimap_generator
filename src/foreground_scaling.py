#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2, os, sys
import numpy as np
from abc import ABC, abstractmethod

def extractImage(path):
    # error handller if the intended path is not found
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE);
    return image

def checkImage(image):
    """
    Args:
        image: input image to be checked
    Returns:
        binary image
    Raises:
        RGB image, grayscale image, all-black, and all-white image

    """
    if len(image.shape) > 2:
        print("ERROR: non-binary image (RGB)");
        sys.exit();

    smallest = image.min(axis=0).min(axis=0); # lowest pixel value; should be 0 (black)
    largest  = image.max(axis=0).max(axis=0); # highest pixel value; should be 1 (white)

    if (smallest == 0 and largest == 0):
        print("ERROR: non-binary image (all black)");
        sys.exit();
    elif (smallest == 255 and largest == 255):
        print("ERROR: non-binary image (all white)");
        sys.exit();
    elif (smallest > 0 or largest < 255 ):
        print("ERROR: non-binary image (grayscale)");
        sys.exit();
    else:
        return True


class FGScale(ABC):
    """
    An abstract base class that enables image erosion or dilation PRE trimap
    Attribute: binary image
    Method: scaling with two inputs: image and iterations
    """
    def __init__(self, image):
        self.image = image;
        
    @abstractmethod
    def scaling(self, image, iteration):
        pass

class Erosion(FGScale):
    def __init__(self, image):
        self.image = image

    def scaling(self, image, erosion):
        erosion = int(erosion)
        kernel = np.ones((3,3), np.uint8)                     ## Design an odd-sized erosion kernel
        image = cv2.erode(image, kernel, iterations=erosion)  ## The number of erosions
        image = np.where(image > 0, 255, image)               ## Any gray-clored pixel becomes white (smoothing)
        # Error-handler to prevent entire foreground annihilation
        if cv2.countNonZero(image) == 0:
            print("ERROR: foreground has been entirely eroded");
            sys.exit();
        return image;

class Dilation(FGScale):
    def __init__(self, image):
        self.image = image

    def scaling(self, image, dilation):
        dilation = int(dilation)
        kernel = np.ones((3,3), np.uint8)                       ## Design an odd-sized erosion kernel
        image  = cv2.dilate(image, kernel, iterations=dilation) ## The number of dilations
        image  = np.where(image > 0, 255, image)                ## Any gray-clored pixel becomes white (smoothing)
        # Error-handler to prevent entire foreground domination
        height = image.shape[0];
        width  = image.shape[1];
        totalpixels = height*width;
        n_white_pix = np.sum(image == 255)
        
        if n_white_pix == totalpixels:
            print("ERROR: foreground has been entirely expanded");
            sys.exit();
        return image;


#############################################
###             TESTING SECTION           ###
#############################################
if __name__ == '__main__':

    path  = "./images/test_images/test_image_12.png"
    image = extractImage(path)

    unit01  = Erosion(image)
    new_image = unit01.scaling(image, 2)

    cv2.imshow('Displayed Image', new_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

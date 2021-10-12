#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2, os, sys
# Input image is a numpy array with pixel value is BGR 
# (opencv default)

#1. grayscale rgb mean and variance
def get_pixel_summary(image):
  img_gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  luminance = img_gray.mean()
  red   = image[:,:,2].mean()
  green = image[:,:,1].mean()
  blue  = image[:,:,0].mean()
  
  gray_var  = img_gray.var()
  red_var   = image[:,:,2].var()
  green_var = image[:,:,1].var()
  blue_var  = image[:,:,0].var()

  return luminance, red, green, blue, gray_var, red_var, green_var, blue_var

#2. distinct pixel rate
def get_dist_pixel_rate(image):
  height, width,_    = image.shape
  dist_pixel = len(np.unique( [str(x) 
      for x in image[:,:,:].reshape(-1, 3).tolist()]))
  dist_pixel_rate = dist_pixel / float(height * width)
  return dist_pixel_rate

#3. colorfulness
def image_colorfulness(image):
  (B, G, R) = cv2.split(image.astype("float"))
  rg = np.absolute(R - G)
  yb = np.absolute(0.5 * (R + G) - B)
  (rbMean, rbStd) = (np.mean(rg), np.std(rg))
  (ybMean, ybStd) = (np.mean(yb), np.std(yb))
  stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
  meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
  colorfulness = stdRoot + (0.3 * meanRoot)
  return colorfulness
  
#4. saturation
def get_saturation(image):
  img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  saturation = img_hsv[:,:,1].mean()
  return saturation

#5 blur
def get_blur(image):
  blur = cv2.Laplacian(image, cv2.CV_64F).var()
  return blur

#6 sharpness
def get_sharpness(image):
  gy, gx = np.gradient(img_gray)
  gnorm = np.sqrt(gx**2 + gy**2)
  sharpness = np.average(gnorm)
  return sharpness

if __name__ == '__main__':
    path = '../images/test_images/test_image_12.png'
    image = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
    cv2.imshow('Displayed Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

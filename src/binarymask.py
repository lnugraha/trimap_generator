import numpy as np
import cv2
import math
import sys, os
import matplotlib.pyplot as plt
from matplotlib.path import Path

def pnpoly(Polygon, vertex):
    """
    Description: decide whether a point is inside or outside a closed polygon
    Input:  a 2-D polygon with at least three distinct points
            a 2-D vertex using (x, y) format
    Output: 0 (if outside) or 1 (if inside or attached to the polygon)
    """
    c = 0                                                                       
    if (len(Polygon) < 3):                                                      
        print("ERROR: polygon requires at least three vertices")                
        sys.exit
    elif (len(vertex) != 2):
        print("ERROR: vertex is not in 2D format")
        sys.exit                                                                

    for i in range(len(Polygon)):
        if (len(Polygon[i]) != 2):
            print("ERROR: vertex of the polygon is not in 2D format")
            sys.exit
    
    check =  Path( Polygon ).contains_point( vertex )
    c = (check is True and 1) or (check is False and 0)
    return c     

def binary_mask(Polygon, AllPixels, savePNG=False, saveTXT=False):
    """
    TODO: Fix this part 
    Description: Generate a binary mask based on a given 2-D contour polygon
    Polygon: The polygon containing contour points
    AllPixels: The generated binary mask
    savePNG: save the generated mask as a .png file
    saveTXT: save the generated mask as a .txt file
    """
    rows = int( math.sqrt(len(AllPixels)) )
    cols = int( math.sqrt(len(AllPixels)) )
    final = np.zeros(rows*cols);

    for i in range(rows):
        for j in range(cols):
            final[i*cols+j] = pnpoly(Polygon, AllPixels[i*cols+j])

    return final

if __name__ == "__main__":
    Polygon = [[0.0, 0.0], [5.0, 0.0], [5.0, 5.0], [0.0, 5.0]]
    # point_00 = pnpoly(Polygon, [2.0, 2.0])
    # point_01 = pnpoly(Polygon, [12.0, 15.0])
    TestPixels = [];
    for i in range(10):
        for j in range(10):
            TestPixels.append( [i,j] )

    results = binary_mask(Polygon, TestPixels)
    # cv2.imshow('img', results)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    test_poly = "./assets/polygons/raw_mask_30.txt"
    test = np.loadtxt(test_poly);
    
    ROI_x = []; ROI_y = []; ROI_z = []; ROI_xy = [];
    for i in range( int( test.size/3 ) ):
        ROI_x.append( test[i][0] )
        ROI_y.append( test[i][1] )
        ROI_z.append( test[i][2] )
        ROI_xy.append([test[i][0], test[i][1]])

    # FIXME
    # RawVoxels= [];
    # for i in range(512):
    #    for j in range (512):
    #        RawVoxels.append( [-275+i*1.074219 , -275+j*1.074219 ]  )
    # check_results = binary_mask(ROI_xy, RawVoxels);
    # plt.scatter(ROI_x, ROI_y, s=2, color='black')
    # plt.show()

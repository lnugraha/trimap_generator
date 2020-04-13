import numpy as np
import sys, os
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
    Description: Generate a binary mask based on a given 2-D contour polygon
    Polygon: The polygon containing contour points
    AllPixels: The generated binary mask
    savePNG: save the generated mask as a .png file
    saveTXT: save the generated mask as a .txt file
    """
    pass

if __name__ == "__main__":
    Polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0]]
    point_00 = pnpoly(Polygon, [2.0, 2.0])
    print(point_00)

    point_01 = pnpoly(Polygon, [12.0, 15.0])
    print(point_01)

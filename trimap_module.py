import cv2, os, sys
import numpy as np

def check_image(image):
    """
    This function checks whether the input image is binary.
    To be completed: optimization in nested for-loop using Cython
    """
    width  = image.shape[0]; height = image.shape[1];

    # So far, input image is converted to grayscale;
    # thus this is not an issue at the moment
    if len(image.shape) > 2:
        print("ERROR: non-binary image (RGB)");
        sys.exit();

    if cv2.countNonZero(image) == 0:
        print("ERROR: non-binary image (all black)");
        sys.exit();
    else:
        for i in range(0,width):
            for j in range (0,height):
                if (image[i,j] == 255 ):
                    print("ERROR: non-binary (all white)");
                    sys.exit();
                elif (image[i,j] != 0 and image[i,j] != 255 ):
                    print("ERROR: non-binary (grayscale)")
                    sys.exit();
                else:
                    return True

def trimap_generate(image, name, size, number, erosion=False):
    """
    This function creates a trimap based on simple dilation algorithm
    Inputs [4]: a binary image (black & white only), name of the image, dilation pixels 
                the last argument is optional; i.e., how many iterations will the image get eroded                 
    Output    : a trimap
    """
    check_image(image);

    pixels    = 2*size + 1;                                     ## Double and plus 1 to have an odd-sized kernel            
    kernel    = np.ones((pixels,pixels),np.uint8)               ## How many pixel of extension do I get

    if erosion is not False:
        erosion = int(erosion)                                    
        erosion_kernel = np.ones((3,3), np.uint8)                 ## Design an odd-sized erosion kernel
        image = cv2.erode(image, erosion_kernel, iterations=erosion)  ## How many erosion do you expect
        image = np.where(image > 0, 255, image)                         ## Any gray-clored pixel becomes white (smoothing)
        # Error-handler to prevent entire foreground annihilation
        if cv2.countNonZero(image) == 0:
            print("ERROR: foreground has been entirely eroded");
            sys.exit();

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

""" Uncomment this part to test the modules above as Python script
if __name__ == '__main__':
    name  = "./images/test_images/test_image_0.png"; # ONLY test_image_0.png shall succeed
    image = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    size = 10;         
    number = name[-5];
    title = "test_image"

    trimap_generate(image, title, size, number, erosion=10);
    print("Here")
"""


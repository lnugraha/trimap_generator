import cv2, os, sys
import numpy as np

################################################
## 03/04/2019                                 ##
## TODO: Find the largest dominant foreground ##
################################################

def print_image(image,title,number):
    """
    Print your image to a text file
    Checking purpose only
    """
    print(title+"_"+number);
    f= open("image.txt","w+")
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            f.write("%d " %image[i,j])
        f.write("\n")
    f.close()

def check_image(image):
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


def trimap(image, name, size, number, erosion=False):
    """
    This function creates a trimap based on simple dilation algorithm
    Inputs [4]: a binary image (black & white only), name of the image, dilation pixels
                the last argument is optional; i.e., how many iterations will the image get eroded
    Output    : a trimap
    """
    check_image(image);
    
    row    = image.shape[0];
    col    = image.shape[1];

    pixels = 2*size + 1;                                     ## Double and plus 1 to have an odd-sized kernel
    kernel = np.ones((pixels,pixels),np.uint8)               ## How many pixel of extension do I get

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

    #############################################
    # Ensures only three pixel values available #
    # TODO: Optimization with Cython            #
    #############################################    
    for i in range(0,row):
        for j in range (0,col):
            if (remake[i,j] != 0 and remake[i,j] != 255):
                remake[i,j] = 127;

    path = "./images/results/"                                  ## Change the directory
    new_name = '{}px_'.format(size) + name + '_{}.png'.format(number);
    cv2.imwrite(os.path.join(path , new_name) , remake)


#############################################
###             TESTING SECTION           ###
#############################################
if __name__ == '__main__':
    path  = "./images/test_images/test_image_9.png";

    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE);
    size = 10;
    number = path[-5];
    title = "test_image"

    trimap(image, title, size, number, erosion=False);

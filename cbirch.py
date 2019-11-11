??? from here until ???END lines may have been inserted/deleted
import math
from skimage import color
from skimage import io
import imageio
import matplotlib.pyplot as plt
import numpy as np
from skimage import color
import cv2 as cv
from mpl_toolkits import mplot3d
import sys

##############
# Globals go here
##############

# This method draws the two vertical lines onto the image
def drawVerticalLine(image, rowValue):

    for y in range(len(image[0]) ):
        image[y][rowValue][0] = 0
        image[y][rowValue][1] = 0
        image[y][rowValue][2] = 0
        

def drawVerticalLine(self, rowValue):

    for x in range(len(self.image[0]) ):
         pass


# Return True if this location exsits 
# in the class's image field
def doesLocationExist(self, x, y):

    if ( x < 0 or y < 0 ):
        return False

    if ( (y
        
            

# This method draws the two horizontal lines onto
# the image
def drawHorizontalLine(columnValue)
    



# This method opens an image from disk and 
# stores a refrence to it in the global var "image"
# The input imageName is a path to the image -
# The image must be in the current directory
def importImage(imageName):

    try:
        image = imageio.imread(imageName)      
        return image
    except:
        print("There was an IO error opening the image")
    
    return None

# This method will import the N-th image in a dataset
def importImage_N(N):
    nameBase = "image_girl/"

    # Create/import the list of all the images
    imageNumber = 0
    if (N < 10):
        imageNumber = "000"
    elif ( N < 100):
        imageNumber = "00"
    elif ( N > 100):
        imageNumber = "0"

    newName = nameBase + str(imageNumber) +  str(N) + str(".jpg")
    newImage = importImage(newName)
    
    return newImage

# This class describes a 2-D histogram of pixel values 
class histogram:
    
    def __init__(self, image, numColorBins):
        
        self.image = image
 
        self.colorBins =  np.zeros(numColorBins)

    # FIX ME FIX ME FIX ME FIX ME FIX ME FIX ME
    # Creates color space histogram in RGB space 
    def processImage_(self):

        # recording the number of occurunces of each color value
        for i in range(len(self.image) ):
            for j in range(len(self.image[i] ) ):
                
                pass

                # self.colorBins[] = 



# This method will display a given image
def display(image):
    plt.imshow(image)
    plt.show()




############ MAIN ###################


display(importImage_N(10 ) )




# inputImage = cv.cvtColor(inputImage, cv.COLOR_BGR2GRAY)


########### MAIN ####################



???END

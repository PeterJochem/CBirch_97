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

    for y in range(len(image ) ):
        image[y][rowValue][0] = 0
        image[y][rowValue][1] = 0
        image[y][rowValue][2] = 0

    return image

def drawHorizontalLine(image, columnValue):

    # Draw the first horizontal line
    for x in range(len(image[0]) ):
        image[columnValue][x][0] = 0
        image[columnValue][x][1] = 0
        image[columnValue][x][2] = 0
    

    return image




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


# This class stores information about a given ellipse
class ellipse:

    # Constructor
    def __init__(self, x, y, sigma):
    
        self.x = x
        self.y = y
        self.sigma = sigma
    
    
    # def computeMinorAxis(self):

    # def computeMajorAxis(self)



# This method will display a given image in grayscale
def display_gray(image):
    
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.resizeWindow('image', 500, 500)
    cv.imshow('image', image)
    cv.waitKey(0) 
    # plt.imshow(image)
    # plt.show()

# This method will display a given image in color
def display_color(image):
    plt.imshow(image)
    plt.show()



# This method will construct the video
def constructVideo(startingImage, startingEllipse, compareFunction):
    
    numImages = 500
    
    # To start, this is the first image 
    priorImage = startingImage
    priorEllipse = startingEllipse
    
    for i in range(2, numImages + 1):
                
        # Get the next image in the set
        newImage = importImage_N(i)

        # Convert the image to grayscale
        image = cv.cvtColor(newImage, cv.COLOR_BGR2GRAY)

        # Get the edges of the image
        image = cv.Canny(image, 100, 300)
        display_gray(image)
    

        # 
        # search(priorImage, newImage)
    

        # Draw the bounding box on the image
        newImage = drawVerticalLine(newImage, 40)
        newImage = drawHorizontalLine(newImage, 40)    
        # Display the image for testing
        display_color(newImage)



############ MAIN ###################

# Import the starting image
startImage = importImage_N(1)

# FIX ME 
# Choose a comparison function

# Create the starting ellipse
constructVideo(startImage, 1, None)






########### MAIN ####################




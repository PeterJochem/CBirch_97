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
ellipseSize = 40
priorImage = None
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


# This method draws a bounding box centered 
# at the point (x,y) and with dimensions height, width
def drawBoundingBox(image, x, y, height, width):
    
    shiftLeft = float(width) / 2.0
    shiftUp = float(height) / 2.0
    
    # Compute the columns to put our horizontal lines
    columnValue1 = y - int(shiftUp)
    columnValue2 = y + int(shiftUp)
   
    # Compute the rows to put the vertical lines
    rowValue1 = x - int(shiftLeft)
    rowValue2 = x + int(shiftLeft)


    # Draw the first horizontal line
    for i in range( x + int(-shiftLeft), x + int(shiftLeft) ):
        image[columnValue1][i][0] = 0
        image[columnValue1][i][1] = 255
        image[columnValue1][i][2] = 0

    # Draw the second horizontal line
    for i in range( x + int(-shiftLeft), x + int(shiftLeft) ):
        image[columnValue2][i][0] = 0
        image[columnValue2][i][1] = 255
        image[columnValue2][i][2] = 0

    
    # Draw the first vertical line
    for i in range( y + int(-shiftUp), y + int(shiftUp) ):
        image[i][rowValue1][0] = 0
        image[i][rowValue1][1] = 255
        image[i][rowValue1][2] = 0
    
    # Draw the second vertical line
    for i in range( y + int(-shiftUp), y + int(shiftUp) ):
        image[i][rowValue2][0] = 0
        image[i][rowValue2][1] = 255
        image[i][rowValue2][2] = 0

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
    def __init__(self, x, y, sigma, scaleFactor):
    
        self.x = x
        self.y = y
        self.sigma = sigma
         
        self.a = scaleFactor * sigma
        self.b = scaleFactor * 1

    
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


# Given an ellipse, compute if the given point is inside the ellipse
# (x,y) is a point in the image
def isInside(myEllipse, x, y):
    

    term1 = ( (myEllipse.x - x)**2) / float(myEllipse.b**2)
    term2 = ( (myEllipse.y - y)**2) / float(myEllipse.a**2)
    
    if ( (term1 + term2) < 1):
        return True


    return False


# This checks that a given (x,y) pair in an image exists 
def isLocation(image, x, y):
    
    if ( len(image) <= y):
        return False

    if ( len(image[0] ) <= x ):
        return False

    return True


# This method takes an ellipse and constructs 
# its sum of square distances (SSD)
def ssd(image, priorEllipse, newEllipse): 
    
    global priorImage

    # Convert the image to grayscale
    grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)   

    # The template's ellipses's location
    x_c = priorEllipse.x 
    y_c = priorEllipse.y 
    
    # How far to search over the image
    width = int(priorEllipse.a) + 10
    height = int(priorEllipse.b) + 10
    
    ssd = 0

    # Traverse a rectangular section of the image
    for y in range( -1 * height, height ):
        for x in range( -1 * width, width ):
            
            # Current pixel in the new search window
            currentX = x_c + x  
            currentY = y_c + y
        
            if ( isLocation(image, currentX, currentY) ):
                if ( isInside(priorEllipse, currentX, currentY) == True):
                    image[currentY][currentX] = 0
                    
                    # Compute the statistic
                    i_new = grayImage[currentY][currentX]
                    
                    i_t = priorImage[currentY][currentX][0]

                    ssd = ssd + (i_new - i_t)**2 

    print("The ssd is " + str(ssd) )
    return image


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
display_color(startImage)

# startImage = drawVerticalLine(startImage, 40)
# startImage = drawHorizontalLine(startImage, 40)

startImage = drawBoundingBox(startImage, 70, 45, 45, 40)
display_color(startImage)


#  def __init__(self, x, y, sigma, scaleFactor):
myEllipse = ellipse(70, 45, 1.2, 20)


priorImage = startImage         
resultImage = ssd(startImage, myEllipse, myEllipse)


display_color(resultImage)

# FIX ME 
# Choose a comparison function

# Create the starting ellipse
# constructVideo(startImage, 1, None)






########### MAIN ####################




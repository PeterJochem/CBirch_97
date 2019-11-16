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

from decimal import * 

##############
# Globals go here
priorImage = None
priorEllipse = None
sigma = 1.2
scaleFactor = 14
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
    

    term1 = float( ( (myEllipse.x - x)**2) ) / float(myEllipse.b**2)
    term2 = float( ( (myEllipse.y - y)**2) ) / float(myEllipse.a**2)
    
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


def drawEllipse(newImage, newEllipse):
    global priorImage

    # The template's ellipses's location
    #x_c = priorEllipse.x 
    #y_c = priorEllipse.y 

    x_c = newEllipse.x
    y_c = newEllipse.y

    # How far to search over the image
    width = int(newEllipse.a) 
    height = int(newEllipse.b) 

    # Traverse a rectangular section of the image
    for y in range( -1 * height, height ):
        for x in range( -1 * width, width ):

            # Current pixel in the new search window
            currentX = int(x_c + x)
            currentY = int(y_c + y)

            if ( isLocation(newImage, currentX, currentY) ):
                if ( isInside(newEllipse, currentX, currentY) == True):

                    newImage[currentY][currentX][0] = 0

    return newImage


# This method takes an ellipse and constructs 
# its sum of square distances (SSD)
def ncc(newImage, priorEllipse, newEllipse):
    
    global priorImage

    x_c = newEllipse.x
    y_c = newEllipse.y

    x_c_old = priorEllipse.x
    y_c_old = priorEllipse.y

    # How far to search over the image
    width = int(priorEllipse.a)
    height = int(priorEllipse.b)
    
    prior_sum = 0
    new_sum = 0
    prior_denom = 0
    new_denom = 0

    my_ncc = 0

    # Traverse a rectangular section of the image
    # Compute the average of each image's section
    for y in range( -1 * height, height ):
        for x in range( -1 * width, width ):

            # Current pixel in the new search window
            currentX = int(x_c + x)
            currentY = int(y_c + y)

            old_x = int(x_c_old + x)
            old_y = int(y_c_old + y)

            # check other location
            if ( isLocation(newImage, currentX, currentY) and isLocation(priorImage, old_x, old_y) ):
                if ( isInside(newEllipse, currentX, currentY) == True):

                    prior_sum = prior_sum + priorImage[old_y][old_x]
                    prior_denom = prior_denom + 1

                    new_sum = new_sum + newImage[currentY][currentX]
                    new_denom = new_denom + 1
    

    # Compute the averages
    prior_avg = float(prior_sum) / float(prior_denom)
    new_avg = float(new_sum) / float(new_denom)

    # Is this the right way to interpet the equation?
    old_hat = 0
    new_hat = 0

    # Traverse the region again
    for y in range( -1 * height, height ):
        for x in range( -1 * width, width ):

            # Current pixel in the new search window
            currentX = int(x_c + x)
            currentY = int(y_c + y)

            old_x = int(x_c_old + x)
            old_y = int(y_c_old + y)

            # check other location
            if ( isLocation(newImage, currentX, currentY) and isLocation(priorImage, old_x, old_y) ):
                if ( isInside(newEllipse, currentX, currentY) == True):
                
                        # Compute the statistic
                        i_new = newImage[currentY][currentX]
                        i_new = i_new - new_avg  

                        
                        i_t = priorImage[old_y][old_x]
                        i_t = i_t - prior_avg 

                        # update normalization terms 
                        old_hat = old_hat + i_t**2
                        new_hat = new_hat + i_new**2

                        
                        my_ncc = my_ncc + (i_new * i_t)


             
    # Normalize the ncc
    my_ncc = my_ncc / math.sqrt( (  (old_hat) * (new_hat)  ) ) 

    # print("The ncc is " + str(my_ncc) )
    return my_ncc



# This method takes an ellipse and constructs 
# its sum of square distances (SSD)
def cc(newImage, priorEllipse, newEllipse):

    global priorImage

    x_c = newEllipse.x
    y_c = newEllipse.y

    x_c_old = priorEllipse.x
    y_c_old = priorEllipse.y

    # How far to search over the image
    width = int(priorEllipse.a)
    height = int(priorEllipse.b)

    cc = 0

    # Traverse a rectangular section of the image
    for y in range( -1 * height, height ):
        for x in range( -1 * width, width ):

            # Current pixel in the new search window
            currentX = int(x_c + x)
            currentY = int(y_c + y)

            old_x = int(x_c_old + x)
            old_y = int(y_c_old + y)

            # check other location
            if ( isLocation(newImage, currentX, currentY) and isLocation(priorImage, old_x, old_y) ):
                if ( isInside(newEllipse, currentX, currentY) == True):

                    # Compute the statistic
                    i_new = newImage[currentY][currentX]

                    # SHOULD THIS BE newIMAGE?? or priorImage???
                    # ???????????? 
                    # Should the coordinates be diffrent   
                    # i_t = priorImage[currentY][currentX] 
                    i_t = priorImage[old_y][old_x]
                    # print(i_t)

                    cc = cc + (i_new * i_t) 

    print("The cc is " + str(cc) )
    return cc



# This method takes an ellipse and constructs 
# its sum of square distances (SSD)
def ssd(newImage, priorEllipse, newEllipse): 
    
    global priorImage
    
    x_c = newEllipse.x
    y_c = newEllipse.y

    x_c_old = priorEllipse.x
    y_c_old = priorEllipse.y

    # How far to search over the image
    width = int(priorEllipse.a) 
    height = int(priorEllipse.b) 
    
    ssd = 0

    # Traverse a rectangular section of the image
    for y in range( -1 * height, height ):
        for x in range( -1 * width, width ):
            
            # Current pixel in the new search window
            currentX = int(x_c + x)  
            currentY = int(y_c + y)
        
            old_x = int(x_c_old + x)
            old_y = int(y_c_old + y)
            
            # check other location
            if ( isLocation(newImage, currentX, currentY) and isLocation(priorImage, old_x, old_y) ):
                if ( isInside(newEllipse, currentX, currentY) == True):
                    
                    # Compute the statistic
                    i_new = newImage[currentY][currentX]

                    # SHOULD THIS BE newIMAGE?? or priorImage???
                    # ???????????? 
                    # Should the coordinates be diffrent   
                    # i_t = priorImage[currentY][currentX] 
                    i_t = priorImage[old_y][old_x]
                    # print(i_t)
        
                    ssd = ssd + ( (i_new - i_t)**2)  

    print("The ssd is " + str(ssd) )
    return ssd


def localSearch_ncc(newImage, stride, totalSearch):

    global priorImage
    global priorEllipse
    global sigma
    global scaleFactor

    x = priorEllipse.x
    y = priorEllipse.y

    offset = np.linspace(0, totalSearch, stride)

    allNums = np.array( [] )
    allEllipses = np.array( [] )

    # For each offset, compute the ssd for the new ellipse
    for i in range(len(offset) ):

        # Shift just the x 
        newE1 = ellipse(x + offset[i], y, sigma, scaleFactor)
        newE2 = ellipse(x - offset[i], y, sigma, scaleFactor)
        num1 = ncc(newImage, priorEllipse, newE1)
        num2 = ncc(newImage, priorEllipse, newE2)

        # Shift the y
        newE3 = ellipse(x, y + offset[i], sigma, scaleFactor)
        newE4 = ellipse(x, y - offset[i], sigma, scaleFactor)
        num3 = ncc(newImage, priorEllipse, newE3)
        num4 = ncc(newImage, priorEllipse, newE4)

        # Shift the x and y - in same directon
        newE5 = ellipse(x + offset[i], y + offset[i], sigma, scaleFactor)
        newE6 = ellipse(x - offset[i], y - offset[i], sigma, scaleFactor)
        num5 = ncc(newImage, priorEllipse, newE5)
        num6 = ncc(newImage, priorEllipse, newE6)

        # Shift the x and y - in opposite directons
        newE7 = ellipse(x + offset[i], y - offset[i], sigma, scaleFactor)
        newE8 = ellipse(x - offset[i], y + offset[i], sigma, scaleFactor)
        num7 = ncc(newImage, priorEllipse, newE7)
        num8 = ncc(newImage, priorEllipse, newE8)

        # Don't shift the window at all
        newE9 = ellipse(x, y, sigma, scaleFactor)
        num9 = ncc(newImage, priorEllipse, newE9)


        nums = np.array( [num1, num2, num3, num4, num5, num6, num7, num8, num9] )
        ellipses = np.array( [newE1, newE2, newE3, newE4, newE5, newE6, newE7, newE8, newE9] )

        allNums = np.append(allNums, nums)
        allEllipses = np.append( allEllipses, ellipses )


    # Traverse each number and find the smallest one
    maxIndex = 0
    maxValue = -1000
    for i in range(len(allNums) ):

        if ( (maxValue) < (allNums[i] ) ):
            maxIndex = i
            maxValue = allNums[i]

    #print("The maxIndex is " + str(maxIndex) )
    #print("The length of allNums is " + str(len(allNums)) )
    # print(allNums[minIndex] )
    desiredEllipse = allEllipses[maxIndex]

    return desiredEllipse



# Search locally 
# stride is the delta in x and y for the next point
# totalSearch is how far in total to search over in both 
# the x and y directions
def localSearch_cc(newImage, stride, totalSearch):

    global priorImage
    global priorEllipse
    global sigma
    global scaleFactor

    x = priorEllipse.x
    y = priorEllipse.y

    offset = np.linspace(0, totalSearch, stride)
    print(offset)

    allNums = np.array( [] )
    allEllipses = np.array( [] )

    # For each offset, compute the ssd for the new ellipse
    for i in range(len(offset) ):

        # Shift just the x 
        newE1 = ellipse(x + offset[i], y, sigma, scaleFactor)
        newE2 = ellipse(x - offset[i], y, sigma, scaleFactor)
        num1 = cc(newImage, priorEllipse, newE1)
        num2 = cc(newImage, priorEllipse, newE2)

        # Shift the y
        newE3 = ellipse(x, y + offset[i], sigma, scaleFactor)
        newE4 = ellipse(x, y - offset[i], sigma, scaleFactor)
        num3 = cc(newImage, priorEllipse, newE3)
        num4 = cc(newImage, priorEllipse, newE4)

        # Shift the x and y - in same directon
        newE5 = ellipse(x + offset[i], y + offset[i], sigma, scaleFactor)
        newE6 = ellipse(x - offset[i], y - offset[i], sigma, scaleFactor)
        num5 = cc(newImage, priorEllipse, newE5)
        num6 = cc(newImage, priorEllipse, newE6)

        # Shift the x and y - in opposite directons
        newE7 = ellipse(x + offset[i], y - offset[i], sigma, scaleFactor)
        newE8 = ellipse(x - offset[i], y + offset[i], sigma, scaleFactor)
        num7 = cc(newImage, priorEllipse, newE7)
        num8 = cc(newImage, priorEllipse, newE8)

        # Don't shift the window at all
        newE9 = ellipse(x, y, sigma, scaleFactor)
        num9 = cc(newImage, priorEllipse, newE9)


        nums = np.array( [num1, num2, num3, num4, num5, num6, num7, num8, num9] )
        ellipses = np.array( [newE1, newE2, newE3, newE4, newE5, newE6, newE7, newE8, newE9] )

        allNums = np.append(allNums, nums)
        allEllipses = np.append( allEllipses, ellipses )


    print("The allNums array is ")
    print(allNums)
    
    # Traverse each number and find the smallest one
    maxIndex = 0
    maxValue = -1000000000000000
    for i in range(len(allNums) ):

        if ( (maxValue) < (allNums[i] ) ):
            maxIndex = i
            maxValue = allNums[i]

    #print("The maxIndex is " + str(maxIndex) )
    #print("The length of allNums is " + str(len(allNums)) )
    # print(allNums[minIndex] )
    desiredEllipse = allEllipses[maxIndex]

    return desiredEllipse




# Search locally 
# stride is the delta in x and y for the next point
# totalSearch is how far in total to search over in both 
# the x and y directions
def localSearch_ssd(newImage, stride, totalSearch):
    
    global priorImage
    global priorEllipse
    global sigma
    global scaleFactor
    
    x = priorEllipse.x
    y = priorEllipse.y

    offset = np.linspace(0, totalSearch, stride)
    
    allNums = np.array( [] )
    allEllipses = np.array( [] )

    # For each offset, compute the ssd for the new ellipse
    for i in range(len(offset) ):
        
        # Shift just the x 
        newE1 = ellipse(x + offset[i], y, sigma, scaleFactor)
        newE2 = ellipse(x - offset[i], y, sigma, scaleFactor)
        num1 = ssd(newImage, priorEllipse, newE1) 
        num2 = ssd(newImage, priorEllipse, newE2)
         
        # Shift the y
        newE3 = ellipse(x, y + offset[i], sigma, scaleFactor)
        newE4 = ellipse(x, y - offset[i], sigma, scaleFactor) 
        num3 = ssd(newImage, priorEllipse, newE3)     
        num4 = ssd(newImage, priorEllipse, newE4)

        # Shift the x and y - in same directon
        newE5 = ellipse(x + offset[i], y + offset[i], sigma, scaleFactor)
        newE6 = ellipse(x - offset[i], y - offset[i], sigma, scaleFactor)
        num5 = ssd(newImage, priorEllipse, newE5)
        num6 = ssd(newImage, priorEllipse, newE6)

        # Shift the x and y - in opposite directons
        newE7 = ellipse(x + offset[i], y - offset[i], sigma, scaleFactor)
        newE8 = ellipse(x - offset[i], y + offset[i], sigma, scaleFactor)
        num7 = ssd(newImage, priorEllipse, newE7)
        num8 = ssd(newImage, priorEllipse, newE8)
            
        # Don't shift the window at all
        newE9 = ellipse(x, y, sigma, scaleFactor)
        num9 = ssd(newImage, priorEllipse, newE9)


        nums = np.array( [num1, num2, num3, num4, num5, num6, num7, num8, num9] )  
        ellipses = np.array( [newE1, newE2, newE3, newE4, newE5, newE6, newE7, newE8, newE9] )

        allNums = np.append(allNums, nums)
        allEllipses = np.append( allEllipses, ellipses )
    

    print("The allNums array is ")
    print(allNums)
    
    # Traverse each number and find the smallest one
    minIndex = 0
    minValue = 10000000000
    for i in range(len(allNums) ):
        
        if ( (minValue) > (allNums[i] ) ):
            minIndex = i
            minValue = allNums[i]
    
    print("The minIndex is " + str(minIndex) )
    print("The length of allNums is " + str(len(allNums)) )
    # print(allNums[minIndex] )
    desiredEllipse = allEllipses[minIndex]
    
    return desiredEllipse


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

startEllipse = ellipse(70, 45, sigma, scaleFactor)
priorEllipse = startEllipse
priorImage = cv.cvtColor(startImage, cv.COLOR_BGR2GRAY)


for i in range(1, 500):

    
    currentImage_color = importImage_N(i)
    currentImage_gray = cv.cvtColor(currentImage_color, cv.COLOR_BGR2GRAY)
   
    # Run it with priorImage - it nails it!
    newEllipse = localSearch_ncc(currentImage_gray, 5, 5)

    # print( str(returnedEllipse.x) + ", " + str(returnedEllipse.y) )
    
    # drawBoundingBox(image, x, y, height, width)
    print(newEllipse.y)
    currentImage_color = drawBoundingBox(currentImage_color, int(newEllipse.x), int(newEllipse.y), 35, 35) 
    # currentImage_color = drawEllipse(currentImage_color, returnedEllipse)
    
    display_color(currentImage_color)

    # Set up the next iteration
    priorEllipse = newEllipse
    priorImage = currentImage_gray












# display_color(resultImage)

# FIX ME 
# Choose a comparison function

# Create the starting ellipse
# constructVideo(startImage, 1, None)






########### MAIN ####################




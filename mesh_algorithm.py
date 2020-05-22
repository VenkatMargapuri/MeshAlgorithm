import cv2
import numpy as np
from collections import defaultdict
import itertools
import math
import random as rng
from statistics import median
#################### Add filepath
OUTPUT_DIR = r""
#####################
hexagonSide = 4.5

# Comptues theh area of hexagon from its side
def ComputeHexagonArea(side):
    
    return (3 * 1.732 * side * side)/2

# Computes the median of a list of values
def ComputeMedian(values):
    values.sort()
    return median(values) 

# Computes the length and width of the seeds based on its median perimeter
def ComputeSeedLengthandWidth(values, hexagonPerimeter, medianPerimeter):
    val1 = values[1][0]
    val2 = values[1][1]
    length = max(val1, val2)
    width = min(val1, val2)
    length = (length * hexagonPerimeter)/ medianPerimeter
    width = (width * hexagonPerimeter)/ medianPerimeter
    return length, width

# Computes the length and width of the seeds based on the min-enclosing circle
def ComputeSeedLengthandWidthCircle(diameter, hexagonPerimeter, medianPerimeter):
    length = (diameter * hexagonPerimeter)/medianPerimeter
    width = length
    return length, width

# Computes teh length ad width of the seeds based on the farthest points on each side
def ComputeLengthandWidthFarthestPt(length, width, hexagonPerimeter, medianPerimeter):
    leng = (length * hexagonPerimeter)/ medianPerimeter
    wid = (width * hexagonPerimeter)/ medianPerimeter
    return leng, wid


#driver code
if __name__ == "__main__":

	#read the input file
	src = cv2.imread("{}\Soy_IMG.jpg".format(OUTPUT_DIR))  
    
	src_copy = src.copy() 
    
# Covert the color image to grayscale    
	src_copy = cv2.cvtColor(src_copy, cv2.COLOR_BGR2GRAY);
        
    
# Creates several copies of the source image to plot different morphometric estimations          
	src_copy2 = src.copy()
    
	src_copy3 = src.copy()    
    
	src_copy4 = src.copy()    
    
	src_copy5 = src.copy()
    
	src_copy6 = src.copy()  
    
	src_copy7 = src.copy()    
    
	src_copy8 = src.copy()  
    
	src_copy9 = src.copy()
    
	src_copy10 = src.copy()    
    
# Computes the area of each hexagon in the mesh based on its side    
	hexagonArea = ComputeHexagonArea(hexagonSide)     
    
# Filters the red, green and blue channels of the image based on pixel intensity    
	red = np.logical_and(150 < src_copy2[:,:,0], src_copy2[:,:,0] < 255)
	green = np.logical_and(150 < src_copy2[:,:,1], src_copy2[:,:,1] < 255)
	blue = np.logical_and(150 < src_copy2[:,:,2], src_copy2[:,:,2] < 255)       
	valid_range = np.logical_and(red, green, blue)
    
# Sets the pixels in valid range identified above to white and others to black    
	src_copy[valid_range] = 255
	src_copy[np.logical_not(valid_range)] = 0
    
	cv2.imwrite("{}/Source.jpg".format(OUTPUT_DIR), src_copy)
    
# perfroms a median blur on the image    
	can_blur = cv2.medianBlur(src_copy, 9)
        
# Performs canny edge detection on the image        
	can = cv2.Canny(can_blur, threshold1=50, threshold2=255)    
            
# Finds contours on the image        
	cont, hier = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
	contourAreas = []    
	contourPerimeters = []    
    
# Find contours which represent the hexagons in the mesh
# It is estimated that the hexagons in the mesh occupy a pixel area of at least 10000
	for i in cont:
		if(cv2.contourArea(i) > 10000):    
			contourAreas.append(cv2.contourArea(i))
			contourPerimeters.append(cv2.arcLength(i, True))                        
			cv2.drawContours(can, [i], -1, (128, 128, 128), -1)
			(x,y),radius = cv2.minEnclosingCircle(i)

			center = (int(x), int(y) - 60)            
			#cv2.putText(can, "{}".format(cv2.arcLength(i, True)), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2,cv2.LINE_AA)            
	cv2.imwrite("{}/src2.jpg".format(OUTPUT_DIR), can)

    
    
# Computes the median area and perimeter of the hexagons in the mesh       
	medianArea = ComputeMedian(contourAreas)
	medianPerimeter = ComputeMedian(contourPerimeters)
    
# Computes the perimeter based on its side    
	hexagonPerimeter = hexagonSide * 6                
    
# Converts the image to grayscale    
	src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  
    
# binary thresholds the image and sets all values below a pixel intensity of 70 to black and above to 255 (white)    
	ret, gray = cv2.threshold(src, 70, 255, cv2.THRESH_BINARY) 
	cv2.imwrite("{}\gray.png".format(OUTPUT_DIR), gray)       
    
# Median blurs the image    
	blur = cv2.medianBlur(gray, 7)
    
# performs canny edge detection on the image    
	edges = cv2.Canny(blur, threshold1=200, threshold2=255)
    
# Performs a morphological closing to close gaps in the image    
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 20))
	edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, rect_kernel)
	cv2.imwrite("{}\struct.png".format(OUTPUT_DIR), edges)       
    
# Finds contours on the image    
	contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cont = []    
	for i,v in enumerate(hierarchy[0]):
		if(v[3] == -1):
			cont.append(contours[i])
            
            
	r = 255
	g = 200
	b = 100
	seed_count = 0
	hull_list = []    
    
    
	rectList = []
    
# Finds the perimeter of each of the contours
	for index, contour in enumerate(cont):
		perimeter = cv2.arcLength(contour, True)
		rect = cv2.minAreaRect(contour) 
        
# Filters the contours based on the area. Only the contours deemed seeds are processed        
		if(cv2.contourArea(contour) > 100):
# Computes the convex hull of the contours        
			hull = cv2.convexHull(contour)  
# Computes the min-area rectangles of the contours to estimate length and width    
			minRect = cv2.minAreaRect(contour)                                     
			minAreaBox = cv2.boxPoints(minRect)                                   
			minAreaBox = np.int0(minAreaBox)            
			cv2.drawContours(src_copy4, [minAreaBox], -1, (r, g, b), 2)                           
			length, width = ComputeSeedLengthandWidth(minRect, hexagonPerimeter, medianPerimeter)                            
			cv2.drawContours(src_copy2, [contour], -1, (r, g, b), 2) 
            
# Computes the area of the seed.            
			seedArea = (cv2.contourArea(contour) * hexagonArea)/(medianArea)
            
            
            
			major_axis = length/2
            
			minor_axis = width/2    
            
			#seedArea = (3.14 * major_axis * minor_axis)
            
			#seedPerimeter = (cv2.arcLength(contour, True) * hexagonPerimeter)/ medianPerimeter            
                        
			seedPerimeter = 2 * 3.14 * (((major_axis * major_axis) + (minor_axis * minor_axis))/2) ** 0.5
            
			#seedPerimeter = cv2.arcLength(contour, True)            
            
# Computes the min-enclosing circle around the contour            
			(x,y),radius = cv2.minEnclosingCircle(contour)            
			minAreaBoxCircle = cv2.circle(src_copy6, (int(x), int(y)), int(radius), (r, g, b), 2)            

# Computes the seed area based on min enclosing circle radius       
			seedAreaCircle = ((3.14 * radius * radius) * hexagonArea)/medianArea
# Computes the seed length and width based on the min-enclosing circle radius            
			seedCircleLength, seedCircleWidth = ComputeSeedLengthandWidthCircle(2 * radius, hexagonPerimeter, medianPerimeter)  
                        
			seedAreaPerimeter = 2 * 3.14 * radius  
            
			center = (int(x), int(y) - 60)
            
# Computes the length and width of seeds based on leftmost-rightmost and topmost-bottommost points on the contours            
			extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
			extRight = tuple(contour[contour[:, :, 0].argmax()][0])
			extTop = tuple(contour[contour[:, :, 1].argmin()][0]) 
			extBottom = tuple(contour[contour[:, :, 1].argmax()][0])              
			Widthpx = math.sqrt((extLeft[0] - extRight[0]) ** 2 + (extLeft[1] - extRight[1]) ** 2)
			Lengthpx = math.sqrt((extTop[0] - extBottom[0]) ** 2 + (extTop[1] - extBottom[1]) ** 2)            
			leng, wid = ComputeLengthandWidthFarthestPt(Lengthpx, Widthpx, hexagonPerimeter, medianPerimeter)

			cv2.line(src_copy9, extLeft, extRight,(255,0,0),5)
			cv2.line(src_copy9, extTop,extBottom,(0,255,0),5)
            

            
            
            
			cv2.putText(src_copy2, "{}".format(seed_count + 1), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 4,cv2.LINE_AA)
			cv2.putText(src_copy3, "{}".format(round(seedArea, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 4,cv2.LINE_AA)
			cv2.putText(src_copy4, "{} - {}".format(round(length, 2), round(width, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 4,cv2.LINE_AA)     
			cv2.putText(src_copy5, "{}".format(round(seedPerimeter, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3,cv2.LINE_AA)       
			cv2.putText(src_copy6, "{}".format(round(seedAreaCircle, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)   
			cv2.putText(src_copy7, "{}".format(round(seedAreaPerimeter, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA) 
			#cv2.putText(src_copy8, "{}".format(round(seedAreaContour, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA) 
			cv2.putText(src_copy9, "{} - {}".format(round(leng, 2), round(wid, 2)), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)               
           

			r = rng.randint(0, 255)
			g = rng.randint(0, 255)
			b = rng.randint(0, 255)
			seed_count = seed_count + 1


	cv2.imwrite("{}\SeedCounts.png".format(OUTPUT_DIR), src_copy2)    
	cv2.imwrite("{}\SeedAreas.png".format(OUTPUT_DIR), src_copy3)
	cv2.imwrite("{}\LengthWidths.png".format(OUTPUT_DIR), src_copy4) 
	cv2.imwrite("{}\SeedPerimeters.png".format(OUTPUT_DIR), src_copy5)    
	cv2.imwrite("{}\seedAreaCircle.png".format(OUTPUT_DIR), src_copy6)    
	cv2.imwrite("{}\seedAreaPerimeter.png".format(OUTPUT_DIR), src_copy7) 
	cv2.imwrite("{}\seedAreaContour.png".format(OUTPUT_DIR), src_copy8)   
	cv2.imwrite("{}\seedCircleLengths.png".format(OUTPUT_DIR), src_copy9)       


from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import imutils


#CONSTANTS DEFINITIONS
#Kernel Size definition for GaussianBlur
KERNEL_X = 3
KERNEL_Y = 3
#Threshold Max and Min Values for Noise Reduction
MIN_TRESH= 70;
MAX_TRESH = 255
#AVG_SIZE refers to visually the smallest cell size compared to the largest. Can be modified.
AVG_SIZE = 10
#CONSIDER MINIMUM CELL and Select how close you want to get the minimum to the avg AVG_SIZE
MIN_AVG_SIZE = 15 

counter = 0
sum = 0
areas = []

# load the image and perform pyramid mean shift filtering
# to aid the thresholding step
image = cv2.imread('Frame2.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_gauss = cv2.GaussianBlur(image, (3,3), 0,0)
image_gray = cv2.cvtColor(image_gauss, cv2.COLOR_BGR2GRAY)
#image_gray = cv2.equalizeHist(image_gray)
image_contours = image.copy()
height, width, channels = image.shape
counter = 0
sum = 0
areas = []

#Adaptive Histogram Equalization
clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(5,5))
cl1 = clahe.apply(image_gray)

#Kernel Definitions
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))

#Threshold and Noise Reduction with dilation and erosion
ret,image_edged = cv2.threshold(cl1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_CLOSE, kernel)
#image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
#image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
#image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
#image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
# image_edged3[0:(height-1),0] = 255
# image_edged3[0:(height-1), (width-1)] = 255
# image_edged3[(height-1),0:(width-1)] = 255
# image_edged3[0,1:(width-1)] = 255

#Find Contours
cnts = cv2.findContours(image_edged3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

for i in cnts:
    #print(cv2.contourArea(i))
    areas.append(cv2.contourArea(i))
    sum = cv2.contourArea(i) + sum
    counter = counter + 1
check = max(areas)
check2 = min(areas)
avg = sum/counter
avg_check = avg + 4*avg
if check > avg_check:
    sum = sum - check
    avg = sum/(counter-1)
minimum = avg/4
maximum = 4 * avg

# cells=[]
# counter = 0
# #Ignore contours that do not satisfy size criteria
# for i in cnts:
#     if cv2.contourArea(i) < minimum or cv2.contourArea(i) > maximum:
#         continue;
#     #obtain moment from cell objects
#     M = cv2.moments(i)
#     #obtain center coordinates and print them
#     cx = int(M['m10']/M['m00'])
#     cy = int(M['m01']/M['m00'])
#     cells.append([cx,cy])
#     #cv2.circle(image_contours, (cx, cy), 5, (0, 255, 0), -1)
#     hull = cv2.convexHull(i)
#     if (cv2.contourArea(i) == 0):
#         cv2.fillPoly(image_edged3, [hull], (0,0,0))
#     else:
#         cv2.fillPoly(image_edged, [hull], (255,255,255))
#     #cv2.drawContours(image_contours,[hull],0,(0,255,0), 2)
#     counter = counter + 1

# image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
# image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
# image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
# image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
# image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
# image_edged3[0:(height-1),0] = 255
# image_edged3[0:(height-1), (width-1)] = 255
# image_edged3[(height-1),0:(width-1)] = 255
# image_edged3[0,1:(width-1)] = 255

# #Find Contours
# cnts = cv2.findContours(image_edged3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# for i in cnts:
#     #print(cv2.contourArea(i))
#     areas.append(cv2.contourArea(i))
#     sum = cv2.contourArea(i) + sum
#     counter = counter + 1
# check = max(areas)
# check2 = min(areas)
# avg = sum/counter
# avg_check = avg + 4*avg
# if check > avg_check:
#     sum = sum - check
#     avg = sum/(counter-1)
# minimum = avg/4
# maximum = 4 * avg

cells=[]
counter = 0
#Ignore contours that do not satisfy size criteria
for i in cnts:
    if cv2.contourArea(i) < minimum or cv2.contourArea(i) > maximum:
        continue;
    #obtain moment from cell objects
    M = cv2.moments(i)
    #obtain center coordinates and print them
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cells.append([cx,cy])
    cv2.circle(image_contours, (cx, cy), 5, (0, 255, 0), -1)
    hull = cv2.convexHull(i)
    if (cv2.contourArea(i) == 0):
        cv2.fillPoly(image_edged3, [hull], (0,0,0))
    else:
        cv2.fillPoly(image_edged, [hull], (255,255,255))
    #cv2.drawContours(image_contours,[hull],0,(0,255,0), 2)
    counter = counter + 1
#Return Results
print(cnts)
print(cells)
print ("Average Value is: %d and cells: %d" %(avg, counter))
numpy_horizontal = np.hstack((image, image_contours))
numpy_horizontal_concat = np.concatenate((image, image_contours), axis = 1)
cv2.imshow("video", numpy_horizontal_concat)
cv2.imshow("edged", image_edged3)
cv2.imshow('first', image_edged)

waitKey(0)
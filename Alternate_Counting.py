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
MIN_TRESH= 180;
MAX_TRESH = 255
#AVG_SIZE refers to visually the smallest cell size compared to the largest. Can be modified.
AVG_SIZE = 3
#CONSIDER MINIMUM CELL and Select how close you want to get the minimum to the avg AVG_SIZE
MIN_AVG_SIZE = 4

counter = 0
sum = 0
areas = []

image1 = cv2.imread('Frame_brighter3.png')
#mage1 = cv2.imread(frame)
height, width, channels = image1.shape
number = np.amax(image1)
#print(number)
#image1 = image1/number
#image1= np.uint8(image1)

image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
#from scipy import ndimage, misc

#misc.imsave('frame2.jpg', image1)
#image1 = ndimage.imread('frame2.jpg', 0)

image_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image_gauss = cv2.GaussianBlur(image_gray,(KERNEL_X,KERNEL_Y), 0,0);
image_contours = image1.copy()

#Adaptive Histogram Equalization
#clahe = cv2.createCLAHE(clipLimit=6, tileGridSize=(8,8))
#cl1 = clahe.apply(image_gray)
#Kernel Definitions for Threshold
kernel = np.zeros((1,1), np.uint8)
kernel2 = np.zeros((1,1), np.uint8)
#Apply morphological modifications
ret, image_edged = cv2.threshold(image_gauss, MIN_TRESH, MAX_TRESH, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
image_edged2 = cv2.dilate (image_edged, kernel, iterations = 3)
#image_edged3 = cv2.erode (image_edged2, kernel2, iterations = 1)
# image_edged3[0:(height-1),0] = 255
# image_edged3[0:(height-1), (width-1)] = 255
# image_edged3[(height-1),0:(width-1)] = 255
# image_edged3[0,1:(width-1)] = 255
#frame_init("cells1.png")

#dist_transform = cv2.distanceTransform(image_edged,cv2.DIST_L2,3)
#ret, sure_fg= cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)

#sure_fg = np.uint8(sure_fg)
#unknown = cv2.subtract(image_edged,sure_fg)


# Marker labelling
#ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
#markers = markers+1

# Now, mark the region of unknown with zero
#markers[unknown==255] = 0

#markers = cv2.watershed(image1,markers)
#image1[markers == -1] = [255,0,0]



#Find Contours
cnts = cv2.findContours(image_edged2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

#Iterate through contours and calculate average cell sixe
for i in cnts:
    #print(cv2.contourArea(i))
    areas.append(cv2.contourArea(i))
    sum = cv2.contourArea(i) + sum
    counter = counter + 1
check = max(areas)
avg = sum/counter
avg_check = avg + AVG_SIZE * avg
if check > avg_check:
    sum = sum - check
    avg = sum/(counter-1)
minimum = avg - MIN_AVG_SIZE * min(areas)
maximum = AVG_SIZE * avg

cells=[]
counter = 0

#Iterate through all contours and rule out those that do not satisfy size criteria
for i in cnts:
    if cv2.contourArea(i) < minimum or cv2.contourArea(i) > maximum:
        continue;
    #obtain moment from cell objects
    M = cv2.moments(i)
    #obtain center coordinates and print them
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cells.append([cx,cy])
    cv2.circle(image_contours, (cx, cy), 5, (0, 0, 0), -1)
    x, y, w, h = cv2.boundingRect(i)
    # draw a green rectangle to visualize the bounding rect
    #cv2.rectangle(image_contours, (x, y), (x+w, y+h), (0, 0, 255), 2)
    # get the min area rect
    rect = cv2.minAreaRect(i)
    box = cv2.boxPoints(rect)
    # convert all coordinates floating point values to int
    #box = np.int0(box)
    # draw a red 'nghien' rectangle
    #cv2.drawContours(image_contours, [box], 0, (255, 0, 0), 2)
    hull = cv2.convexHull(i)
    cv2.drawContours(image_contours,[hull],0,(0,0,255), 2)
    counter = counter + 1

#Return Results
print(cnts)
print(cells)
print ("Average Value is: %d and cells: %d" %(avg, counter))
cv2.imshow("gaussian", image_gauss)
cv2.imshow("Contours", image_contours)
cv2.imshow("Thresh", image_edged)

cv2.waitKey(0)

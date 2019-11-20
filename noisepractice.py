
#By Mayra Banuelos

import numpy as np
import matplotlib.pyplot as plt
import cv2
import imutils

video=cv2.VideoCapture('cellvid11.avi')
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

def onChange(trackbarValue):
    video.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    err,image = video.read()

    image_contours = image.copy()
    height, width, channels = image.shape
    counter = 0
    sum = 0
    areas = []

    #Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(5,5))
    lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    cl1 = clahe.apply(l)
    lab3 = cv2.merge((cl1, a, b))
    #cl2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    #image_gray = cv2.cvtColor(cl2, cv2.COLOR_BGR2GRAY)
    #image_gauss = cv2.GaussianBlur(image_gray, (3,3), 0,0)

    #Kernel Definitions
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    #kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    #kernel = np.ones((2,4), np.uint8)
    kernel2 = np.ones((2,2), np.uint8)

    #Threshold and Noise Reduction with dilation and erosion
    ret, image_edged = cv2.threshold(cl1, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_edged = cv2.bitwise_not(image_edged)
    image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_CLOSE, kernel)
    #image_edged3=cv2.morphologyEx(image_edged2, cv2.MORPH_OPEN, kernel)
    #image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    #image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
    #image_edged2 = cv2.erode (image_edged, kernel2, iterations = 2)
    image_edged3 = cv2.dilate (image_edged3, kernel2, iterations = 3)
    image_edged3 = cv2.bitwise_not(image_edged3)
    image_edged3[0:(height-1),0] = 255
    image_edged3[0:(height-1), (width-1)] = 255
    image_edged3[(height-1),0:(width-1)] = 255
    image_edged3[0,1:(width-1)] = 255

    #Find Contours
    cnts = cv2.findContours(image_edged3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for i in cnts:
    	#print(cv2.contourArea(i))
    	areas.append(cv2.contourArea(i))
    	sum = cv2.contourArea(i) + sum
    	counter = counter + 1
    check = max(areas)
    avg = sum/counter
    avg_check = avg + 4*avg
    if check > avg_check:
    	sum = sum - check
    	avg = sum/(counter-1)
    minimum = avg - 10 * min(areas)
    maximum = 5 * avg

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
    	cv2.drawContours(image_contours,[hull],0,(0,255,0), 2)
    	counter = counter + 1

    #Return Results
    print(cnts)
    print(cells)
    print ("Average Value is: %d and cells: %d" %(avg, counter))
    # cv2.imshow("Original", image)
    cv2.imshow("Contoursl", image_contours)
    cv2.imshow("Edged3", image_edged3)
    # cv2.imshow("Edged1", image_edged)
    cv2.imshow("CONTRASTED", cl1)
    #cv2.imshow("GAUSS", image_gauss)

    pass

cv2.namedWindow('video')
#Put in for loop to move automatically and to start again
cv2.createTrackbar( 'start', 'video', 0, length, onChange )

onChange(0)
cv2.waitKey(0)

start = cv2.getTrackbarPos('start','video')
end   = cv2.getTrackbarPos('end','video')

video.set(cv2.CAP_PROP_POS_FRAMES,start)

video.set(cv2.CAP_PROP_POS_FRAMES,start)

while(video.isOpened()):
  ret, img=video.read()
  if video.get(cv2.CAP_PROP_POS_FRAMES) >= end:
     break
  cv2.imshow("Cell_Video", gray)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

##################################################
## Software interface and backend created to track division and 
## trajectory of Drosophila Melanogaster Cells.
##################################################
## Author: Mayra Banuelos
## Copyright: Copyright 2018, CLONETIFY-IT
## Credits: Sarai Aquino, Ted
## Version: 1.0.0
## Mmaintainer: Mayra Banuelos
## Status: Currently being translated to Python3 and PyQt5
##################################################

import numpy as np
import cv2
import imutils

def counter(video_file, frame_no):

    frame_no = frame_no
    cap = cv2.VideoCapture(video_file)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.get(7) #video_name is the video being called
    cap.set(1,(frame_no)) # Where frame_no is the frame you want
    ret, image = cap.read() 
    dst = np.zeros(shape=(5,2))

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_gauss = cv2.GaussianBlur(image, (3,3), 0,0)
    image_gray = cv2.cvtColor(image_gauss, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.equalizeHist(image_gray)
    cv2.normalize(image_gray, dst, 0, 255, cv2.NORM_MINMAX)
    image_contours = image.copy()
    height, width, channels = image.shape
    counter = 0
    sum = 0
    areas = []

    #Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(8,8))
    cl1 = clahe.apply(image_gray)

    #Kernel Definitions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    #Threshold and Noise Reduction with dilation and erosion
    ret,image_edged = cv2.threshold(cl1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)

    image_edged3[0:(height-1),0] = 255
    image_edged3[0:(height-1), (width-1)] = 255
    image_edged3[(height-1),0:(width-1)] = 255
    image_edged3[0,1:(width-1)] = 255

    #Find Contours
    cnts = cv2.findContours(image_edged3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for i in cnts:
        #print(cv2.contourArea(i))
        if cv2.contourArea(i) == 0:
            continue;
        else:
            areas.append(cv2.contourArea(i))
            sum = cv2.contourArea(i) + sum
            #sum_t = sum_t + (cv2.contourArea(i) * cv2.contourArea(i))
            counter = counter + 1

    areas.remove(max(areas))
    import math

    avg = sum/counter
    sum_sq = 0

    #Calculate overall variance
    for i in range(len(areas)):
        var = sum - areas[i]
        var_sq = var * var
        sum_sq = sum_sq + var_sq

    var_avg = sum_sq/counter
    variance = math.sqrt(var_avg)/counter

    minimum = (math.sqrt(variance) * math.sqrt(counter/2))
    r = math.sqrt(avg) 
    maximum = avg + variance
    print(areas, sum, variance, avg, maximum, minimum)

    cells=[]
    counter = 0

    #Ignore contours that do not satisfy size criteria
    for i in cnts:
        if cv2.contourArea(i) < minimum or cv2.contourArea(i) > maximum:
            continue

        #obtain moment from cell objects
        M = cv2.moments(i)
        #obtain center coordinates and print them
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #self.cells.append([cx,cy])
        #cv2.circle(image_contours, (cx, cy), 5, (0, 255, 0), -1)
        hull = cv2.convexHull(i)
        x, y, w, h = cv2.boundingRect(i)
        #print(x,y,w,h)
        width = x + w
        height = y + h
        if width < (5*height):
            area = cv2.contourArea(i)
            cells.append([x,y,width,height, cx, cy, area])
            # draw a green rectangle to visualize the bounding rect
            #cv2.rectangle(image_contours, (x, y), (x+w, y+h), (0, 0, 255), 2)
            #cv2.drawContours(image_contours,[hull],0,(0,255,0), 2)
            #counter = counter + 1
        else:
            pass
    pass

    n = len(cells)
    total = n - 1
    delete=[]

    for j in range(0, total):
        for k in range(j+1, n):
            if abs(cells[j][4] - cells[k][4]) < 15:
                if abs(cells[j][5] - cells[k][5]) < 15:
                    if cells[j][6] > cells[k][6]:
                        delete.append(k)
                    else:
                        delete.append(j)
                
    print(delete)
    for i in sorted(delete, reverse=True):
        del cells[i]

    size = len(cells)
    for m in range(0, size):
        cx = int(cells[m][4])
        cy = int(cells[m][5])
        cv2.circle(image_contours, (cx, cy), 5, (34,255,34), -1)
        counter = counter + 1

    #cv2.imshow('edged', image_edged3)

    return(image_contours, counter, cells, height, width, avg)


def onMouse(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x=%d, y=%d'%(x,y))

def drawRectangle(image, array):
    for j in range(0,len(array)):
        x, y, w, h = array[j][0], array[j][1], array[j][2], array[j][3]
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    return image


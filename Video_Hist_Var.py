
#By Mayra Banuelos

import numpy as np
import cv2
import imutils
       
video=cv2.VideoCapture('cellvid13.wmv')
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

def onChange(trackbarValue):
    video.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    err,image = video.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_gauss = cv2.GaussianBlur(image, (3,3), 0,0)
    #image_gauss = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    image_gray = cv2.cvtColor(image_gauss, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.equalizeHist(image_gray)
    #cv2.normalize(image_gray, image_gray, 0, 255, cv2.NORM_MINMAX)
    image_contours = image.copy()
    height, width, channels = image.shape
    counter = 0
    sum = 0
    areas = []

    #Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(5,5))
    cl1 = clahe.apply(image_gray)

    #Kernel Definitions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))

    #Threshold and Noise Reduction with dilation and erosion
    ret,image_edged = cv2.threshold(cl1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
    #image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel)

    image_edged3[0:(height-1),0] = 255
    image_edged3[0:(height-1), (width-1)] = 255
    image_edged3[(height-1),0:(width-1)] = 255
    image_edged3[0,1:(width-1)] = 255

    #Find Contours
    cnts = cv2.findContours(image_edged3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
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

    for i in range(len(areas)):
        var = sum - areas[i]
        var_sq = var * var
        sum_sq = sum_sq + var_sq
        #print(sum_sq)

    var_avg = sum_sq/counter
    variance = math.sqrt(var_avg)/counter
    #print(math.sqrt(var_avg)/counter)
    #variance = math.sqrt(sum_t - sum)
    #avg_variance = variance / (counter-1)
    
    # check = avg + avg_variance
    # check2 = avg - avg_variance 

    # avg_check = avg + 4*avg
    # if check > avg_check:
    #   sum = sum - check
    #   avg = sum/(counter-1)
    minimum = (math.sqrt(variance) * math.sqrt(counter/2)) 
    #minimum =  avg/20
    #minimum = avg - (avg/(2*check2))
    maximum = avg + variance
    print(areas, sum, variance, avg, maximum, minimum)

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
        x, y, w, h = cv2.boundingRect(i)
        print(x,y,w,h)
        # draw a green rectangle to visualize the bounding rect
        #cv2.rectangle(image_contours, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #cv2.drawContours(image_contours,[hull],0,(0,255,0), 2)
        counter = counter + 1

    #Return Results
    #print(cnts)
    print(cells)
    print ("Average Value is: %d and cells: %d" %(avg, counter))
    #numpy_horizontal = np.hstack((image, image_contours))
    #numpy_horizontal_concat = np.concatenate((image, image_contours), axis = 1)
    #cv2.imshow("video", numpy_horizontal_concat)
    cv2.imshow("video", image_contours)

    #subset = onMouse()
    cv2.imshow('first', image_edged3)
    pass

cv2.namedWindow('video')
#Put in for loop to move automatically and to start again
cv2.createTrackbar( 'start', 'video', 0, length, onChange)
cv2.createTrackbar( 'end', 'video', length, 0, onChange )


def onMouse(event, x,y, flags, param):
    subset = []
    if event == cv2.EVENT_LBUTTONDOWN:
        
        print('x=%d, y=%d'%(x,y))
        for i in range (0,len(cells)):    
            if x > cells[i][0]:
                if y < cells[i][1]:
                    subset.append(cells[i])
                else:
                    pass
            else:
                pass
    print(subset)

cv2.setMouseCallback('video', onMouse)

onChange(0)
cv2.waitKey(0)

start = cv2.getTrackbarPos('start','video')
end   = cv2.getTrackbarPos('end','video')

video.set(cv2.CAP_PROP_POS_FRAMES,start)
video.set(cv2.CAP_PROP_POS_FRAMES,start)

while(video.isOpened()):
  ret, image =video.read()
  if video.get(cv2.CAP_PROP_POS_FRAMES) >= end:
     break
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

import numpy as np
import cv2
import imutils

def counting(file):
    #CONSTANTS DEFINITIONS
    MIN_TRESH= 70;
    MAX_TRESH = 255

    counter = 0
    sum = 0
    areas = []
    dst = np.zeros(shape=(5,2))

    image1 = cv2.imread(file)
    height, width, channels = image1.shape
    number = np.amax(image1)
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    #image_gauss = cv2.fastNlMeansDenoisingColored(image1, None, 10, 10, 7, 21)
    image_gauss = cv2.GaussianBlur(image1, (3,3), 0,0);
    image_gray = cv2.cvtColor(image_gauss, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.normalize(image_gray, dst, 0, 255, cv2.NORM_MINMAX)
    image_contours = image1.copy()

    #Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=6, tileGridSize=(8,8))
    cl1 = clahe.apply(image_gray)

    #Kernel Definitions for Threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    #Apply morphological modifications
    ret, image_edged = cv2.threshold(cl1, MIN_TRESH, MAX_TRESH, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #image_edged2 = cv2.dilate(image_edged, kernel, iterations = 3)
    #image_edged3 = cv2.erode (image_edged, kernel2, iterations = 5)
    image_edged3= cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3= cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3= cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
    image_edged3=cv2.morphologyEx(image_edged3, cv2.MORPH_CLOSE, kernel2)
    #image_edged3= cv2.morphologyEx(image_edged, cv2.MORPH_OPEN, kernel)


    image_edged3[0:(height-1),0] = 255
    image_edged3[0:(height-1), (width-1)] = 255
    image_edged3[(height-1),0:(width-1)] = 255
    image_edged3[0,1:(width-1)] = 255

    #Find Contours
    cnts = cv2.findContours(image_edged3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]


    #CONSIDER MINIMUM CELL and Select how close you want to get the minimum to the avg AVG_SIZE
    sumVariance = 0
    sum_t = 0

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

    minimum = (math.sqrt(variance) * (math.sqrt(counter/math.pi))) 
    maximum = avg + variance
    print(areas, sum, variance, avg, maximum, minimum)

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
        area = cv2.contourArea(i)
        cells.append([cx,cy,area])
        # cv2.circle(image_contours, (cx, cy), 5, (34,255,34), -1)
        # x, y, w, h = cv2.boundingRect(i)
        # # draw a green rectangle to visualize the bounding rect
        # #cv2.rectangle(image_contours, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # # get the min area rect
        # rect = cv2.minAreaRect(i)
        # box = cv2.boxPoints(rect)
        # # convert all coordinates floating point values to int
        # box = np.int0(box)
        # # draw a red 'nghien' rectangle
        # #cv2.drawContours(image_contours, [box], 0, (255, 0, 0), 2)
        # hull = cv2.convexHull(i)
        # #cv2.drawContours(image_contours,[hull],0,(0,0,0), 2)
        # #cv2.fillPoly(image_edged3, [hull], (0,0,0))
        # counter = counter + 1

    n = len(cells)
    print(n)
    total = n - 1
    delete=[]

    for j in range(0, total):
        for k in range(j+1, n):
            if abs(cells[j][0] - cells[k][0]) < 15:
                if abs(cells[j][1] - cells[k][1]) < 15:
                    if cells[j][2] > cells[k][2]:
                        delete.append(k)
                    else:
                        delete.append(j)
                
    print(delete)
    for i in sorted(delete, reverse=True):
        del cells[i]

    size = len(cells)
    print(size)
    for m in range(0, size):
        cx = int(cells[m][0])
        cy = int(cells[m][1])
        cv2.circle(image_contours, (cx, cy), 5, (34,255,34), -1)
        counter = counter + 1

    #Return Results
    #print(cnts)
    #print(cells)
    print ("Average Value is: %d and cells: %d" %(avg, counter))

    #cv2.waitKey(0)
    return image_contours, counter
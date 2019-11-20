import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import imutils


# Read image
im_in = cv2.imread("cells1.png", cv2.IMREAD_GRAYSCALE);
image_contours = im_in.copy()
# Threshold.
# Set values equal to or above 220 to 0.
# Set values below 220 to 255.

th, im_th = cv2.threshold(im_in, 150, 255, cv2.THRESH_BINARY_INV);

# Copy the thresholded image.
im_floodfill = im_th.copy()

# Mask used to flood filling.
# Notice the size needs to be 2 pixels than the image.
h, w = im_th.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Floodfill from point (0, 0)
cv2.floodFill(im_floodfill, mask, (0,0), 255);

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#kernel = np.ones((3,3))
im_floodfill2 = cv2.erode(im_floodfill, kernel, iterations = 1)

# # Invert floodfilled image
# im_floodfill_inv = cv2.bitwise_not(im_floodfill)
#
# # Combine the two images to get the foreground.
# im_out = im_th | im_floodfill_inv

# Display images.
cv2.imshow("Original Image", im_in)
cv2.imshow("Thresholded Image", im_th)
cv2.imshow("Floodfilled Image", im_floodfill)
cv2.imshow("Dilated", im_floodfill2)
# cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
# cv2.imshow("Foreground", im_out)


counter = 0
sum = 0
areas = []

# image_edged3[0:(height-1),0] = 255
# image_edged3[0:(height-1), (width-1)] = 255
# image_edged3[(height-1),0:(width-1)] = 255
# image_edged3[0,1:(width-1)] = 255

#Find Contours
cnts = cv2.findContours(im_floodfill2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

for i in cnts:
	#print(cv2.contourArea(i))
	areas.append(cv2.contourArea(i))
	sum = cv2.contourArea(i) + sum
	counter = counter + 1
check = max(areas)
avg = sum/counter
avg_check = avg + 3*avg
if check > avg_check:
	sum = sum - check
	avg = sum/(counter-1)
minimum = avg - 4 * min(areas)
maximum = 3 * avg

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
	cv2.circle(image_contours, (cx, cy), 5, (0, 0, 0), -1)
	hull = cv2.convexHull(i)
	cv2.drawContours(image_contours,[hull],-1,(0,0,0), 2)
	counter = counter + 1

#Return Results
print(cnts)
print(cells)
print ("Average Value is: %d and cells: %d" %(avg, counter))
cv2.imshow("Contoursl", image_contours)

cv2.waitKey(0)

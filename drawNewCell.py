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

def draw(video_file, frame_no, cells):
    video=cv2.VideoCapture(video_file)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_no = frame_no
    cap = cv2.VideoCapture(video_file)
    cap.get(7) #video_name is the video being called
    cap.set(1,(frame_no)) # Where frame_no is the frame you want
    #print(frame_no)
    ret, image = cap.read()
    image_contours = image.copy()

    for i in range(0,len(cells)):
    	cx = int(cells[i][4])
    	cy = int(cells[i][5])
    	cv2.circle(image_contours, (cx, cy), 5, (0, 255, 0), -1)
    	#cv2.rectangle(cap, (cells[i][0], cells[i][1]), (cells[i][2], cells[i][3]), (0, 255, 0), 3)
    cv2.imwrite('temp.png', image_contours) 
    return image_contours

import cv2
import numpy as np

cap = cv2.VideoCapture('C:/Users/mbanu/Desktop/698 Presentation/Latest Files/cellvid11.avi')

while(cap.isOpened()):
    # Take each frame
    ret, frame = cap.read()
    if ret:
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # define range of blue color in HSV
        lower_green = np.array([25,189,118])
        upper_green = np.array([95,255,198])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
#cv2.destroyAllWindows()

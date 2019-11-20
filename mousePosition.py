import cv2
import sys
from collections import deque
import numpy as np
import imutils
import math
import saveCoordinates
import plot_path
import time

def track(file, array, position, file_no):
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # Set up tracker
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[0]

    #Assign Tracker
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()

    # Read video
    video = cv2.VideoCapture(file)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    c = file_no

    video.set(cv2.CAP_PROP_POS_FRAMES,position)
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Define an initial bounding box
    x, y, w, h = array[0][0], array[0][1], array[0][2], array[0][3]
    bbox = (x, y, w-x, h-y)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(gray, bbox)
    pts =[]
    coordinates = []
    X=[]
    Y=[]
    endposition = position + 30

    while position < endposition:
        k = cv2.waitKey(5) & 0xff

        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        position = position + 1
        #video.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(gray)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(gray, p1, p2, (255,0,0), 2, 1)
            center = p2
            x = math.ceil((int(bbox[0] + bbox[2]))/2)
            y = math.ceil((int(bbox[1] + bbox[3]))/2)
            pts.append(center)

        else :
            # Tracking failure
            cv2.putText(gray, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        for i in range(1, len(pts)):
            if pts[i -1 ] is None or pts[i] is None:
                continue
            cv2.line(gray, pts[i - 1], pts [i], ((5 + 6*i) ,0, (60 + 8*i)), 3)
            initial = pts[i-1]
            end = pts[i]
            x1 = pts[i-1][0]
            y1 = pts[i-1][1]
            separator =','
            #first_point = separator.join(x2)
            x2 = pts[i][0]
            y2 = pts[i][1]
            coordinates.append(initial)
            coordinates.append(end)
            X.append(x1)
            X.append(x2)
            Y.append(y1)
            Y.append(y2)

        # Display tracker type on frame
        cv2.putText(gray, " Tracking", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        cv2.putText(gray, "FPS : " + str(int(fps)), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display result
        h, w, l = gray.shape
        new_h = 2*h
        new_w = 2*w
        gray = cv2.resize(gray, (new_h, new_w))
        cv2.imshow("CLONETIFY-IT TRACKING", gray)
        time.sleep(0.002)

        # Exit if ESC pressed
        k = cv2.waitKey(2) & 0xff
        if k == 27 : break

    saveCoordinates.save(coordinates, file, c) 
    return (X, Y)


import numpy as np
import cv2

def extraction(video_file, frame_no):
    frame_no = frame_no
    cap = cv2.VideoCapture(video_file)
    cap.get(7) #video_name is the video being called
    cap.set(1,(frame_no-1)) # Where frame_no is the frame you want
    #print(frame_no)
    ret, frame = cap.read() 
    #cv2.imwrite("%dFrame%d.png"%(vide_file,frame_no), frame)
    # Read the frame
    #cv2.imshow('Extracted Frame', frame) 
    return frame
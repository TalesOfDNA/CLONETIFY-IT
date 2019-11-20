import sys
import time as t
import cv2
# Check if OpenCV module is installed
# otherwise stop the application

# try:
#     import cv2
# except ImportError as e:
#     #print("Fatal Error: Could not import OpenCV, %d", %e)
#     exit(-1)
# else:
#     print("Using ")

CURRENT_FRAME_FLAG = cv2.CAP_PROP_POS_FRAMES
TOTAL_FRAMES_FLAG = cv2.CAP_PROP_FRAME_COUNT
WIN_NAME = "Frame Grabber"
POS_TRACKBAR = "pos_trackbar"
# VIDEO_PATH = None

# try:
#     VIDEO_PATH = sys.argv[1]
# except IndexError as e:
#     #print (HELP_MESSAGE)
#     exit(-1)

# grab a VideoCapture object
cap = cv2.VideoCapture('cellvid11.avi')

# check if the video has been correctly opened
if not cap.isOpened():
    print ("Fatal Error: Could not open the specified file.")
    exit(-1)

#try to read a frame
ret, frame = cap.read()

if not ret:
    print ("Fatal Error: Could not read/decode frames from specified file.")
    exit(-1)

def save_image():
    filename = "image_%0.5f.png" % t.time()
    cv2.imwrite(filename, frame)

# STEP 1
# openCV function to create a named window
cv2.namedWindow(WIN_NAME) 

# STEP 2
def seek_callback(x):
    # we want to change the value of the frame variable in the global scope
    global frame
    # by getting the position of the trackbar
    i = cv2.getTrackbarPos(POS_TRACKBAR, WIN_NAME)
    # and skipping to the selected frame
    cap.set(CURRENT_FRAME_FLAG, i-1)
    _, frame = cap.read()
    # we then update the window
    cv2.imshow(WIN_NAME, frame)

# STEP 3
# we create the trackbar in the main window by using
# cv2.createTrackbar(trackbar_name: string, window_name: string,
#                    initial_value: int, max_value: int,
#                    callback_function: callable object)
cv2.createTrackbar(POS_TRACKBAR, WIN_NAME, 0, int(cap.get(TOTAL_FRAMES_FLAG)), seek_callback)    

# STEP 4
# we define a mouse callback function. According to OpenCV docs
# it must take the following parameters:
# event  -> an integer flag describing the event which was triggered
# x, y   -> mouse x and y coordinates when the event was triggered
# flags  -> additional flags
# params -> optional parameters passed to the callback function

def mouse_callback(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDBLCLK:
        save_image()

# STEP 5
cv2.setMouseCallback(WIN_NAME, mouse_callback)

def skip_frame_generator(df):

    def skip_frame():
        global frame
        # get the current frame position
        cf = cap.get(CURRENT_FRAME_FLAG) - 1
        # skip of df frames
        cap.set(CURRENT_FRAME_FLAG, cf+df)
        # update the trackbar position
        cv2.setTrackbarPos(POS_TRACKBAR, WIN_NAME, int(cap.get(CURRENT_FRAME_FLAG)))
        # read and update the frame
        _, frame = cap.read()

    return skip_frame

actions = dict()

actions[ord("D")] = skip_frame_generator(10)
actions[ord("d")] = skip_frame_generator(1)
actions[ord("a")] = skip_frame_generator(-1)
actions[ord("A")] = skip_frame_generator(-10)
actions[ord("q")] = lambda: exit(0)
actions[ord("s")] = save_image

def dummy():
    pass

while True:
    
    # shows the image
    cv2.imshow(WIN_NAME, frame)
    # waits for key stroke
    key = cv2.waitKey(0) & 0xFF
    # calls a function in the actions dictionary
    # according to the pressed key.
    # If that key doesn't exist, the dummy function 
    # will be called
    actions.get(key, dummy)()
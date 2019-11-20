import cv2
video=cv2.VideoCapture('cellvid7.avi')
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

def onChange(trackbarValue):
    video.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    err,img = video.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cv2.imshow('video',gray)
    pass

cv2.namedWindow('video')
cv2.createTrackbar( 'start', 'video', 0, length, onChange )
cv2.createTrackbar( 'end'  , 'video', 100, length, onChange )

onChange(0)
cv2.waitKey()

start = cv2.getTrackbarPos('start','video')
end   = cv2.getTrackbarPos('end','video')

video.set(cv2.CAP_PROP_POS_FRAMES,start)

video.set(cv2.CAP_PROP_POS_FRAMES,start)

while(video.isOpened()):
  ret, img=video.read()
  if video.get(cv2.CAP_PROP_POS_FRAMES) >= end:
     break
  #cv2.imshow("Cell_Video", gray)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

drawing = False # true if mouse is pressed
tracking = False
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy,jx,jy = -1, -1, -1, -1

def BBoxFromPoints(ix, iy, jx, jy):
    #find abs of width and length

    width = abs(jx -ix)
    length = abs(jy-iy)

    bbox = (ix, iy, width, length)
    return bbox

def draw_rectangle(event,x,y,flags,param):
    global ix,iy,jx,jy,drawing,mode, tracking
    
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        print('button down')

    elif event == cv2.EVENT_MOUSEMOVE:
        jx,jy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        tracking = True
        jx,jy = x,y
        bbox = BBoxFromPoints(ix, iy, jx, jy)
        ok = tracker.init(frame, bbox)
        print('button up')

s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

#get source video from webcam
source = cv2.VideoCapture(s)

#create window
win_name = "Tracker"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Tracker", draw_rectangle)

#create loop updating window
tracker = cv2.TrackerMIL.create()

while cv2.waitKey(1) != 27: #Escape
    has_frame, old_frame = source.read()
    
    frame = cv2.flip(old_frame, 1)
    if not has_frame:
        break
    if drawing:
        cv2.rectangle(frame,(ix,iy),(jx,jy),(0,255,0),1)

    elif tracking:

        timer = cv2.getTickCount()

        fps = cv2.getTickFrequency() /(cv2.getTickCount() - timer)

        ok, bbox = tracker.update(frame)

        cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])),
                      (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                      (0,255,0),1)
    

    cv2.imshow(win_name, frame)

cv2.destroyWindow(win_name)
#display current frame + rectangle annotations




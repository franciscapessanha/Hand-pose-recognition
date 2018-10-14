import cv2 as cv
import numpy as np
from sample_skin_color import *

# c) ===================
cap = cv.VideoCapture(0)

sampled = False

while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    frame = cv.flip(frame, 1)

    frame = cv.resize(frame, (0, 0), None, .50, .50) #resize with a scale factor of 0.5 
    frame = cv.medianBlur(frame,5)

    key = cv.waitKey(1) #display frame for 1ms
    if key == 27:
        break # esc to quit
    elif key == 115:
        samples = get_samples(frame)
        sampled = True

    if not sampled:
      draw_sample_rectangles(frame)
    else:
     hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

     mask = cv.inRange(hsv_frame, samples[0], samples[1])
     cv.imshow('mask', mask)

     
     #median: 
     mask_filtered = cv.medianBlur(mask,5)

     #closing with disk
     #kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
     #mask_filtered = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
     
     mask_filtered = cv.cvtColor(mask_filtered, cv.COLOR_GRAY2BGR)
     
     frame = np.concatenate((frame, mask_filtered), axis=1)
    
    cv.imshow('Project', frame)
     
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

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

    key = cv.waitKey(1) #display frame for 1ms
    if key == 27:
        break # esc to quit
    elif key == 115:
        samples = get_samples(frame)
        sampled = True

    if not sampled:
      draw_sample_rectangles(frame)
    else:
      masked_frame = cv.inRange(frame, samples[0], samples[1])
      masked_frame = cv.cvtColor(masked_frame , cv.COLOR_GRAY2BGR)
      frame = np.concatenate((frame, masked_frame), axis=1)
    cv.imshow('Project', frame)
    
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

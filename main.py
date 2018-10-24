import cv2 as cv
import numpy as np
import sys
from sample_skin_color import draw_sample_rectangles, get_samples
from calibrate_mask import create_calibrate_window, get_calibrate_values, show_calibration_window, calcute_mask
from helpers import concatenate_frames

if len(sys.argv) > 1:
  videoCaptureDevice = int(sys.argv[1])
else:
  videoCaptureDevice = 0

cap = cv.VideoCapture(videoCaptureDevice)

sampled = False
calibrated = False
calibrate_window = False

while(True):
  # Capture frame-by-frame
  _, frame = cap.read()
  
  frame = cv.flip(frame, 1)

  frame = cv.resize(frame, (0, 0), None, .50, .50) # Resizes frane with a scale factor of 0.5

  key = cv.waitKey(1) # Waits for user key press

  if key == 27: # Esc to quit
    break
  elif key == 13:
    if not sampled:
      samples = get_samples(frame)
      sampled = True

    if calibrate_window:
      cv.destroyWindow("Calibrate")
      calibrate_window = False

    calibrated_values = get_calibrate_values(samples)
    calibrated = True
  elif key == 99 and sampled: # c to calibrate
    create_calibrate_window()
    calibrate_window = True

  if not sampled:
    draw_sample_rectangles(frame)
  elif calibrate_window:
    mask = show_calibration_window(frame, samples)
  else:
    mask = calcute_mask(frame, calibrated_values)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    
    frame = concatenate_frames(frame, mask)
  
  cv.imshow('Project', frame)

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
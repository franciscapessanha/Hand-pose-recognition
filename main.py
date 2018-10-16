import cv2 as cv
import numpy as np
from sample_skin_color import draw_sample_rectangles, get_samples
from calibrate_mask import create_calibrate_window, get_calibrate_values, show_calibration_window, calcute_mask
from helpers import concatenate_frames

cap = cv.VideoCapture(0)

sampled = False
calibrated = False

while(True):
  # Capture frame-by-frame
  _, frame = cap.read()
  frame = cv.flip(frame, 1)

  frame = cv.resize(frame, (0, 0), None, .50, .50) # Resizes frane with a scale factor of 0.5

  key = cv.waitKey(1) # Waits for user key press

  if key == 27: # Esc to quit
    break
  elif not sampled and key == 115: # s to sample values in sample squares
    samples = get_samples(frame)
    create_calibrate_window()
    sampled = True
  elif not calibrated and sampled and key == 13: # Enter to calibrate values permenently
    calibrated_values = get_calibrate_values(samples)
    cv.destroyWindow("Calibrate")
    calibrated = True

  if not sampled and not calibrated:
    draw_sample_rectangles(frame)
  elif sampled and not calibrated:
    mask = show_calibration_window(frame, samples)
  else:
    mask = calcute_mask(frame, calibrated_values)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    
    frame = concatenate_frames(frame, mask)
  
  cv.imshow('Project', frame)

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

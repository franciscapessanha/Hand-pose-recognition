import cv2 as cv
import numpy as np
from sample_skin_color import draw_sample_rectangles, get_samples
from calibrate_mask import create_calibrate_window, get_calibrate_values, get_default_values, show_calibration_window, calcute_mask
from helpers import concatenate_frames

cap = cv.VideoCapture(0)

sampled = False
calibrated = False

while(True):
  # Capture frame-by-frame
  _, frame = cap.read()
  frame = cv.flip(frame, 1)

  # frame = cv.resize(frame, (0, 0), None, .50, .50) # Resizes frane with a scale factor of 0.5

  key = cv.waitKey(1) # Waits for user key press

  if key == 27: # Esc to quit
    break
  elif not calibrated and not sampled and key == 13:
    samples = get_samples(frame)
    calibrated_values = get_default_values(samples)
    sampled = True
    calibrated = True
  elif not sampled and key == 99: # c to calibrate
    samples = get_samples(frame)
    create_calibrate_window()
    sampled = True
  elif not calibrated and sampled and key == 13: # Enter to calibrate values permenently
    calibrated_values = get_calibrate_values(samples)
    cv.destroyWindow("Calibrate")
    calibrated = True

  if calibrated:
    print(calibrated_values)

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

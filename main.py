import cv2 as cv
import numpy as np
import sys
from sample_skin_color import draw_sample_rectangles, get_samples
from calibrate_window import create_calibrate_window, get_calibrate_values, show_calibration_window
from calculate_mask import get_mask
from helpers import concatenate_frames

state = 'start'

def format_frame(frame):
  frame = cv.flip(frame, 1)
  frame = cv.resize(frame, (640,360)) #this way every video will have the same dimension - and so the kernels will be right!
  return frame

def enter_pressed():
  if state == 'start':
    return
  return

def main():
  if len(sys.argv) > 1:
    videoCaptureDevice = int(sys.argv[1])
  else:
    videoCaptureDevice = 0

  cap = cv.VideoCapture('hand.mp4')

  sampled = False
  calibrated = False
  calibrate_window = False

  while(True):
    # Capture frame-by-frame
    _, frame = cap.read()

    frame = format_frame(frame)

    key = cv.waitKey(35) # Waits for user key press ~ 32 frames/s

    if key == 27: # Esc to quit
      break
    elif key == 13:
      if not sampled:
        #samples = get_samples(frame)
        r = cv.selectROI(frame)
        sample = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        cv.imshow('sample', sample)
        sampled = True

      if calibrate_window:
        cv.destroyWindow("Calibrate")
        calibrate_window = False

      calibrated_values = get_calibrate_values(sample)
      calibrated = True
    elif key == 99 and sampled: # c to calibrate
      create_calibrate_window()
      calibrate_window = True

    if not sampled:
      draw_sample_rectangles(frame)
    elif calibrate_window:
      mask = show_calibration_window(frame, samples)
    else:
      mask_with_contours, mask = get_mask(frame, calibrated_values)
      #mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
      
      frame = concatenate_frames(frame, mask_with_contours)
    
    cv.imshow('Project', frame)

  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()

if __name__ == "__main__":
  main()
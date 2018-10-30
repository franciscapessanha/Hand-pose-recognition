import cv2 as cv
import numpy as np
from calculate_mask import get_mask
from display import *

title = 'Hand Labeling v0.1'
state = 'start'
sample = None
threshold = None

def get_frame_rate(video_capture_source, video_capture):
  if type(video_capture_source) == int:
    return 1
  else:
    return video_capture.get(cv.CAP_PROP_FPS)

def format_frame(frame, video_capture_source):
  if type(video_capture_source) == int: # Video Capture Device is a web camera
    frame = cv.flip(frame, 1)

  frame = cv.resize(frame, (640,360)) #this way every video will have the same dimension - and so the kernels will be right!
  return frame

def enter_pressed(frame):
  global state, threshold, sample
  if state == 'start':
    cv.destroyWindow(title + ' - Press ENTER to sample')
    sample, threshold = open_selector_window(frame)
    state = 'labeling'
  elif state == 'calibrating':
    cv.destroyWindow(calibrate_window_title)
    state = 'labeling'

def s_key_pressed(frame):
  global state, threshold, sample
  if state == 'labeling':
    sample, threshold = open_selector_window(frame)

def c_key_pressed():
  global state
  if state == 'labeling':
    cv.destroyWindow(title)
    create_calibration_window()
    state = 'calibrating'

def handle_key(key, frame):
  if key == 27: # Esc key pressed
    return False
  elif key == 13: # Enter key pressed
    enter_pressed(frame)
  elif key == 99: # C key pressed
    c_key_pressed()
  elif key == 115: # S key pressed
    s_key_pressed(frame)

  return True

def handle_display(frame):
  global state
  if state == 'start':
    cv.imshow(title + ' - Press ENTER to sample', frame)
  elif state == 'labeling':
    mask_with_contours, _ = get_mask(frame, threshold)
    cv.imshow(title, mask_with_contours)
  elif state == 'calibrating':
    open_calibration_window(frame, sample)

def label_video(video_capture_source):
  cap = cv.VideoCapture(video_capture_source)
  frame_rate = get_frame_rate(video_capture_source, cap)

  while(True):
    # Capture frame-by-frame
    _, frame = cap.read()

    frame = format_frame(frame, video_capture_source)

    if not handle_key(cv.waitKey(35), frame): 
      break

    handle_display(frame)

  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()
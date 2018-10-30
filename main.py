import cv2 as cv
import sys
import numpy as np
from calculate_mask import get_mask
from display import *
from helpers import is_int

title = 'Hand Labeling v0.1'
state = 'start'
sample = None
threshold = None

def get_frame_rate(video_capture_source, video_capture):
  if type(video_capture_source) == int:
    return 1
  else:
    return int(video_capture.get(cv.CAP_PROP_FPS))

def format_frame(frame, video_capture_source):
  if type(video_capture_source) == int: # Video Capture Device is a web camera
    frame = cv.flip(frame, 1)

  frame = cv.resize(frame, (640,360)) #this way every video will have the same dimension - and so the kernels will be right!
  return frame

def format_image(image):
  return cv.resize(image, (640,360)) #this way every video will have the same dimension - and so the kernels will be right!


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
    cv.destroyWindow(title)
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
    if frame is None:
      break

    frame = format_frame(frame, video_capture_source)

    if not handle_key(cv.waitKey(frame_rate), frame): 
      break

    handle_display(frame)

  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()

def label_image(image_source):
  while(True):
    image = cv.imread(image_source)
    image = format_image(image)

    if not handle_key(cv.waitKey(1), image): 
      break

    handle_display(image)

def handle_arguments():
  if len(sys.argv) == 1:
    label_video(0)
  elif len(sys.argv) == 2:
    if is_int(sys.argv[1]):
      label_video(int(sys.argv[1]))
    else:
      if sys.argv[1].endswith('.mp4'):
        label_video(sys.argv[1])
      elif sys.argv[1].endswith('.jpg') or sys.argv[1].endswith('.png'):
        label_image(sys.argv[1])

if __name__ == "__main__":
  handle_arguments()
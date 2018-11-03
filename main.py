import cv2 as cv
import sys
import numpy as np
import math
from calculate_mask import get_mask
from display import *
from helpers import is_int

state = 'start'
sample = None
frame_rate = 1
video_frame_rate = 1

def get_frame_rate(video_capture_source, video_capture):
  '''Returns frame rate of the video if it's a video file
  
  Arguments:
    video_capture_source -- File name or code for the video capture source
    video_capture {VideoCaptureObject} -- The opened video capture object
  '''
  
  global video_frame_rate, frame_rate
  if not type(video_capture_source) == int:
    video_frame_rate = int(video_capture.get(cv.CAP_PROP_FPS))
    frame_rate = video_frame_rate

def format_frame(frame, video_capture_source):
  '''Formats the frame to have specific dimensions, so the kernels applied are correct
  
  Arguments:
    frame {Mat} -- Frame to be formatted
    video_capture_source -- File name or code for the video capture source
  
  Returns:
    Mat -- Properly formatted frame
  '''

  if type(video_capture_source) == int: # Video Capture Device is a web camera
    frame = cv.flip(frame, 1)

  new_size = get_new_size(frame)
  frame = cv.resize(frame, (new_size[1],new_size[0]))
  return frame

def format_image(image):
  '''Formats a frame to have specific dimensions, so that the kernels applied are correct
  
  Arguments:
    image {Mat} -- Image to be formatted  
  
  Returns:
    Mat -- Properly formatted image
  '''

  new_size = get_new_size(image)
  return cv.resize(image, (new_size[1],new_size[0]))

def get_new_size(image):
  '''Returns the resize dimentions for the input image
  
  Arguments:
    image {Mat} -- Image that is to be recized
  
  Returns:
    List -- A List with the new width and height of the image
  '''

  size = image.shape
  size = list(size)
  if size[0] >= size[1]:
    size[1] = int(size[1] * (640/size[0]))
    size[0] = 640
  
  elif size[0] < size[1]:
    size[0] = int(size[0] * (640/size[1]))
    size[1] = 640
  return size

def enter_pressed(frame):
  '''Handles what happens when the enter key is pressed during program execution,
  if in starting state opens sample window,
  if in calibration state closes calibration window
  
  Arguments:
    frame {Mat} -- The current frame being labeled
  '''

  global state, sample
  if state == 'start':
    cv.destroyWindow(title + ' - Press ENTER to sample')
    sample = open_sample_window(frame)
    state = 'labeling'
  elif state == 'calibrating':
    cv.destroyWindow(calibrate_window_title)
    state = 'labeling'

def s_key_pressed(frame):
  '''Handles what happens when the s key is pressed during program execution,
  if in labeling state opens sample window
  
  Arguments:
    frame {Mat} -- The current frame being labeled
  '''

  global state, sample
  if state == 'labeling':
    cv.destroyWindow(title)
    sample = open_sample_window(frame)

def c_key_pressed():
  '''Handles what happens when the c key is pressed during program execution,
  if in labeling state opens calibration window
  
  Arguments:
    frame {Mat} -- The current frame being labeled
  '''

  global state
  if state == 'labeling':
    cv.destroyWindow(title)
    create_calibration_window()
    state = 'calibrating'

def space_pressed():
  '''Handles what happens when the space key is pressed during program execution,
  pauses the video being labeled and freezes in current frame
  '''

  global state, frame_rate
  if state == 'labeling':
    frame_rate = 0
    state = 'paused'
  elif state == 'paused':
    frame_rate = video_frame_rate
    state = 'labeling'

def handle_key(key, frame):
  '''Calls functions to handle user keypress
  
  Arguments:
    key {KeyPressCode} -- The key pressed by the user
    frame {Mat} -- The current frame being labeled
  
  Returns:
    Boolean -- False if user presses the escape key, to shutdown execution
  '''

  global frame_rate
  if key == 27: # Esc key pressed
    return False
  elif key == 32: # Space key pressed
    space_pressed()
  elif key == 13: # Enter key pressed
    enter_pressed(frame)
  elif key == 99: # C key pressed
    c_key_pressed()
  elif key == 115: # S key pressed
    s_key_pressed(frame)

  return True

def handle_display(frame):
  '''Handles what window is being displayed depending on current state
  
  Arguments:
    frame {Mat} -- The current frame being labeled
  '''

  global state
  if state == 'start':
    cv.imshow(title + ' - Press ENTER to sample', frame)
  elif state == 'labeling':
    open_label_image_window(frame)
  elif state == 'calibrating':
    open_calibration_window(frame, sample)

def label_video(video_capture_source):
  '''Main loop for video labeling execution
  
  Arguments:
    video_capture_source -- File name or code for the video capture source
  '''

  cap = cv.VideoCapture(video_capture_source)
  get_frame_rate(video_capture_source, cap)

  while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    if frame is None:
      print('Video ended. Closing...')
      break

    frame = format_frame(frame, video_capture_source)
    if not handle_key(cv.waitKey(frame_rate), frame):
      break

    handle_display(frame)

  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()

def label_image(image_source):
  '''Main loop for video labeling execution
  
  Arguments:
    image_source {String} -- File name for the image being labeled
  '''

  global state
  while(True):
    image = cv.imread(image_source)
    image = format_image(image)

    if state == 'calibrating':
      running = 1
    else:
      running = 0

    if not handle_key(cv.waitKey(running), image): 
      break

    handle_display(image)

def handle_arguments():
  '''Handles arguments passed on by the user to the program,
  if no arguments are passed, it opens the default video capture source from the machine,
  if an int argument is passed, it opens that specific video capture source,
  if a string argument is passed, and it ends with ".mp4", ".jpg" or ".png", it opens the file passed
  '''

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
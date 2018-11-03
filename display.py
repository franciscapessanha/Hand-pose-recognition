import cv2 as cv
import numpy as np
from sample_skin_color import calculate_mask_thresholds
from calculate_mask import get_mask
from calculate_contours import find_contours, crop_mask, fill_contours
from calculate_fingers import get_fingers
from helpers import save_list_to_file, load_list_from_file

hue_offset = 60
sat_offset_high = 60
sat_offset_low = 50

thresholds = None

title = 'Hand Labeling v0.3'
calibrate_window_title = 'Calibrating - Press ENTER to confirm'

def set_low_hue_threshold(value):
  thresholds[0][0] = value

def set_high_hue_threshold(value):
  thresholds[1][0] = value

def set_low_sat_threshold(value):
  thresholds[0][1] = value

def set_high_sat_threshold(value):
  thresholds[1][1] = value


def create_calibration_window():
  '''Creates the calibration and initiates the trackbars inside'''

  cv.namedWindow(calibrate_window_title)
  cv.createTrackbar('Hue Low Threshold', calibrate_window_title, thresholds[0][0], 180, set_low_hue_threshold)
  cv.createTrackbar('Hue High Threshold', calibrate_window_title, thresholds[1][0], 180, set_high_hue_threshold)
  cv.createTrackbar('Sat Low Threshold', calibrate_window_title, thresholds[0][1], 255, set_low_sat_threshold)
  cv.createTrackbar('Sat High Threshold', calibrate_window_title, thresholds[1][1], 255, set_high_sat_threshold)

def load_thresholds():
  '''Loads the values of the mask thresholds from a local thresholds file'''

  global thresholds
  thresholds = load_list_from_file('thresholds')

def save_thresholds():
  '''Saves the values of the mask thresholds to a local thresholds file'''

  save_list_to_file(thresholds, 'thresholds')

def get_mask_thresholds(sample):
  '''Returns the mask threshold values from a given sample
  
  Arguments:
    sample {Mat} -- Sample to be used to 
  
  Returns:
    List -- Low and high threshold values
  '''
  global thresholds
  thresholds = calculate_mask_thresholds(sample)
  return thresholds

def open_calibration_window(frame, sample):
  '''Opens the calibration window
  
  Arguments:
    frame {Frame} -- The current frame being labeled
    sample {Mat} -- Sampled portion of the image from where to calculate mask thresholds
  '''
  mask = get_mask(frame, thresholds)
  contours = find_contours(mask)
  mask = fill_contours(contours, mask)
  mask = crop_mask(contours, mask)
  cv.imshow(calibrate_window_title, mask)

def open_sample_window(frame):
  '''Opens the sample window
  
  Arguments:
    frame {Frame} -- The current frame being labeled
  
  Returns:
    Mat -- The user selected samples
    List -- Low and high threshold values calculated from the sample
  '''
  window_title = 'Select a large portion of the skin color'
  r = cv.selectROI(window_title, frame, False)
  sample = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
  cv.destroyWindow(window_title)
  if len(sample) == 0:
    print('Please select a valid region')
    return open_sample_window(frame)
  get_mask_thresholds(sample)
  save_thresholds()
  return sample

def open_label_image_window(frame):
  '''Opens window that displays the image being labeled
  
  Arguments:
    frame {Mat} -- The frame being labeled
  '''

  mask = get_mask(frame, thresholds)
  frame_copy, text = get_fingers(mask, frame)
  add_string_frame(frame_copy, text)
  cv.imshow(title, frame_copy)


def add_string_frame(frame, string):
  '''Adds text to the bottom left of the given frame
  
  Arguments:
    frame {Mat} -- Frame to add the string
    string {String} -- Text to be added
  '''

  bottom_point = (5, frame.shape[0] - 5)
  text_size = cv.getTextSize(string, cv.FONT_HERSHEY_SIMPLEX, 1.5, 2)
  cv.rectangle(frame, (0, frame.shape[0]), (bottom_point[0] + text_size[0][0], bottom_point[1] - text_size[0][1] - 5), (255,255,255), -1 )
  cv.putText(frame, string, bottom_point, cv.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 2)
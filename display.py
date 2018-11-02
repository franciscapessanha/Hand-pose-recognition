import cv2 as cv
import numpy as np
from sample_skin_color import calculate_mask_thresholds
from calculate_mask import get_mask

hue_offset = 60
sat_offset_high = 60
sat_offset_low = 50

calibrate_window_title = 'Calibrating - Press ENTER to confirm'

def set_sat_offset_low(value):
  '''Sets the low saturation offset value, called by the associated calibration trackbar
  
  Arguments:
    value {Int} -- Value to be set
  '''

  global sat_offset_low
  sat_offset_low = value

def set_sat_offset_high(value):
  '''Sets the high saturation offset value, called by the associated calibration trackbar
  
  Arguments:
    value {Int} -- Value to be set
  '''

  global sat_offset_high
  sat_offset_high = value

def set_hue_offset(value):
  '''Sets the hue offset value, called by the associated calibration trackbar
  
  Arguments:
    value {Int} -- Value to be set
  '''

  global hue_offset
  hue_offset = value

def create_calibration_window():
  '''Creates the calibration and initiates the trackbars inside'''

  cv.namedWindow(calibrate_window_title)
  cv.createTrackbar('Hue Offset', calibrate_window_title, hue_offset, 100, set_hue_offset)
  cv.createTrackbar('Sat Offset High', calibrate_window_title, sat_offset_high, 100, set_sat_offset_high)
  cv.createTrackbar('Sat Offset Low', calibrate_window_title, sat_offset_low, 100, set_sat_offset_low)

def get_mask_thresholds(sample):
  '''Returns the mask threshold values from a given sample
  
  Arguments:
    sample {Mat} -- Sample to be used to 
  
  Returns:
    List -- Low and high threshold values
  '''

  return calculate_mask_thresholds(sample, hue_offset/100, sat_offset_low/100, sat_offset_high/100)

def open_calibration_window(frame, sample):
  '''Opens the calibration window
  
  Arguments:
    frame {Frame} -- The current frame being labeled
    sample {Mat} -- Sampled portion of the image from where to calculate mask thresholds
  '''

  mask = get_mask(frame, get_mask_thresholds(sample))
  cv.imshow(calibrate_window_title, mask)

def open_sample_window(frame):
  '''Opens the sample window
  
  Arguments:
    frame {Frame} -- The current frame being labeled
  
  Returns:
    Mat -- The user selected samples
    List -- Low and high threshold values calculated from the sample
  '''

  r = cv.selectROI(frame)
  sample = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
  cv.destroyWindow('ROI selector')
  return sample, get_mask_thresholds(sample)

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
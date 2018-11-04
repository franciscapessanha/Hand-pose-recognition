import cv2 as cv
import numpy as np

def get_mask(frame, thresholds):
  '''Returns a binary mask from a given frame and thresholds
  
  Arguments:
    frame {Mat} -- Frame used to calculate mask
    thresholds {List} -- Low and hight threshold values for hue, saturation and value
  
  Returns:
    Mat -- Binary mask
  '''

  filtered_frame = filter_frame(frame)
  hsv_frame = cv.cvtColor(filtered_frame, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_frame, tuple(thresholds[0]), tuple(thresholds[1]))
  mask = filter_mask(mask)
  return mask

def filter_frame(frame):
  '''Filters a frame for better image processing, by applying an histogram equalization and a median blur
  
  Arguments:
    frame {Mat} -- The frame to be filtered
  
  Returns:
    Mat -- The filtered frame
  '''
  filtered_frame = cv.medianBlur(frame, 9)
  return filtered_frame

def filter_mask(mask):
  '''Filters a mask for better image processing, by applying a dilation and median blur
  
  Arguments:
    mask {Mat} -- Binary mask
  
  Returns:
    Mat -- Filtered mask
  '''

  kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
  mask = cv.dilate(mask,kernel_ellipse, iterations = 2)
  mask = cv.medianBlur(mask, 9)
  return mask

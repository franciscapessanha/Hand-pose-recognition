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

  adjusted_frame = adjust_gamma(frame, gamma = 1.5) # reduzir as sombras - torna tudo mais homogeneo
  filtered_frame = cv.medianBlur(adjusted_frame, 9)
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

def adjust_gamma(frame, gamma = 1.0):
  '''Applies a non linear grey level transformation
  
  Arguments:
    frame {Frame} -- The frame where the equalization is applied
  
  Keyword Arguments:
    gamma {float} -- transformation constant (default: {1.0})
  
  Returns:
    Mat -- Frame with transformation applied
  '''

  invGamma = 1.0 / gamma
  table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)])
  return cv.LUT(frame.astype(np.uint8), table.astype(np.uint8))

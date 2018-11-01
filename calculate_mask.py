import cv2 as cv
import numpy as np

def get_mask(original_frame, values):
  filtered_frame = filter_frame(original_frame)
  hsv_frame = cv.cvtColor( filtered_frame, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_frame, *values)
  mask = filter_mask(mask)
  cv.imshow("final mask", mask)
  return mask

def filter_frame(original_frame):
  adjusted_frame = adjust_gamma(original_frame, gamma = 1.5) # reduzir as sombras - torna tudo mais homogeneo
  filtered_frame = cv.medianBlur(adjusted_frame,9)
  return filtered_frame

def filter_mask(mask):
  kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
  mask = cv.morphologyEx(mask,cv.MORPH_CLOSE, kernel_ellipse)
  mask = cv.medianBlur(mask,9)
  mask = cv.dilate(mask,kernel_ellipse, iterations = 2)
  mask = cv.medianBlur(mask, 9)
  return mask

def adjust_gamma(image, gamma=1.0):
  invGamma = 1.0 / gamma
  table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)])
  return cv.LUT(image.astype(np.uint8), table.astype(np.uint8))


  

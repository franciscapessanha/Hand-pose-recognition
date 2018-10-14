import cv2 as cv
import numpy as np
from sample_skin_color import calculate_sample_values

def nothing(x):
  pass

def create_calibrate_window():
  cv.namedWindow("Calibrate")
  cv.createTrackbar("Hue Offset", "Calibrate", 30, 100, nothing)
  cv.createTrackbar("Sat Offset", "Calibrate", 30, 100, nothing)

def get_calibrate_values(samples):
  hue_offset = cv.getTrackbarPos("Hue Offset", "Calibrate")/100
  sat_offset = cv.getTrackbarPos("Sat Offset", "Calibrate")/100
  return calculate_sample_values(*samples, hue_offset, sat_offset)

def calcute_mask(frame, values):
  frame = cv.medianBlur(frame, 5)
  hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_frame, *values)

  mask_filtered = cv.medianBlur(mask, 3)
  cv.imshow('Before removing noise', mask)
 
  mask_filtered = remove_noise(mask_filtered)

  mask_filtered = cv.medianBlur(mask_filtered, 3)

  return mask_filtered

def show_calibration_window(frame, samples):
  mask = calcute_mask(frame, get_calibrate_values(samples))
  cv.imshow('Calibrate', mask)

  return cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

def remove_noise(mask):
  mask_filtered = mask
  nlabels, labels, contours , centroids  = cv.connectedComponentsWithStats(mask)
  for label in range(1, nlabels):
    x,y,w,h,size = contours[label]

    if size <= mask.size * 0.025: #if area < 2.5% of the total area - is noise
         mask_filtered[y:y+h, x:x+w] = 0

  return mask_filtered

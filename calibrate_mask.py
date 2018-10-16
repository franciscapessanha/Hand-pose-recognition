import cv2 as cv
import numpy as np
from sample_skin_color import calculate_sample_values

sat_offset_low = 30
sat_offset_high = 30
hue_offset = 30

def set_sat_offset_low(value):
  global sat_offset_low
  sat_offset_low = value

def set_sat_offset_high(value):
  global sat_offset_high
  sat_offset_high = value

def set_hue_offset(value):
  global hue_offset
  hue_offset = value

def nothing(x):
  pass

def create_calibrate_window():
  cv.namedWindow("Calibrate")
  cv.createTrackbar("Hue Offset", "Calibrate", hue_offset, 100, set_hue_offset)
  cv.createTrackbar("Sat Offset High", "Calibrate", sat_offset_high, 100, set_sat_offset_high)
  cv.createTrackbar("Sat Offset Low", "Calibrate", sat_offset_low, 100, set_sat_offset_low)

def get_calibrate_values(samples):
  return calculate_sample_values(*samples, hue_offset/100, sat_offset_low/100, sat_offset_high/100)

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

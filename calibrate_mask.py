import cv2 as cv
from sample_skin_color import calculate_sample_values

def nothing(x):
  pass

def create_calibrate_window():
  cv.namedWindow("Calibrate")
  cv.createTrackbar("Hue Offset", "Calibrate", 30, 100, nothing)
  cv.createTrackbar("Sat Offset", "Calibrate", 80, 100, nothing)

def get_calibrate_values(samples):
  hue_offset = cv.getTrackbarPos("Hue Offset", "Calibrate")/100
  sat_offset = cv.getTrackbarPos("Sat Offset", "Calibrate")/100
  return calculate_sample_values(*samples, hue_offset, sat_offset)

def calcute_mask(frame, values):
  frame = cv.medianBlur(frame,5)
  hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

  mask = cv.inRange(hsv_frame, *values)

  #closing with disk
  #kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
  #mask_filtered = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

  return cv.medianBlur(mask,5)

def show_calibration_window(frame, samples):
  mask = calcute_mask(frame, get_calibrate_values(samples))
  cv.imshow('Calibrate', mask)

  return cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

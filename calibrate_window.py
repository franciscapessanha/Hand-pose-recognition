import cv2 as cv
import numpy as np
from sample_skin_color import calculate_sample_values
from calculate_mask import get_mask

hue_offset = 60
sat_offset_high = 60
sat_offset_low = 50

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

def show_calibration_window(frame, samples):
  mask = calcute_mask(frame, get_calibrate_values(samples))
  cv.imshow('Calibrate', mask)

  return cv.cvtColor(mask, cv.COLOR_GRAY2BGR)



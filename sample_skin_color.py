import cv2 as cv
import numpy as np

def calculate_mask_thresholds(sample):
  '''Calculates mask thresholds from a given sample
  
  Arguments:
    sample {Sample} -- The sample from where it will calculate thresholds
  
  Returns:
    List -- List with the low and high HSV thresholds
  '''

  sample = cv.cvtColor(sample, cv.COLOR_BGR2HSV)
  
  hsv_mean = cv.mean(sample)
  hsv_mean = [int(hsv_mean[0]), int(hsv_mean[1]), int(hsv_mean[2])]

  hue_offset = 10
  sat_low_offset = 20
  sat_high_offset = 50

  
  hue_low_thresh = hsv_mean[0] - hue_offset if hsv_mean[0] - hue_offset > 0 else 0
  sat_low_thresh = hsv_mean[1] - sat_low_offset if hsv_mean[1] - sat_low_offset > 0 else 0

  hue_high_thresh = hsv_mean[0] + hue_offset if hsv_mean[0] + hue_offset < 255 else 255
  sat_high_thresh = hsv_mean[1] + sat_high_offset if hsv_mean[1] + sat_high_offset < 255 else 255
  
  return [[hue_low_thresh, sat_low_thresh, 0], [hue_high_thresh, sat_high_thresh, 255]]
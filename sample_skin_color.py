import cv2 as cv

def calculate_mask_thresholds(sample, offset_hue, offset_sat_low, offset_sat_high):
  sample = cv.cvtColor(sample, cv.COLOR_BGR2HSV)
  sample = cv.medianBlur(sample, 5)
  hue, sat, value = cv.split(sample)

  offset_val = 0.50 # alterar

  min_val, max_val, min_loc, max_loc = cv.minMaxLoc(hue)

  hue_low_thresh = (1 - offset_hue) * min_val
  if hue_low_thresh < 0:
    hue_low_thresh = 0

  hue_high_thresh = (1 + offset_hue) * max_val
  if hue_high_thresh > 180:
    hue_high_thresh = 180

  sat_low_thresh = (1 - offset_sat_low) * sat.item(tuple(reversed(min_loc)))
  value_low_thresh = (1- offset_val) * value.item(tuple(reversed(min_loc)))
  if sat_low_thresh < 0:
    sat_low_thresh = 0

  sat_high_thresh = (1 + offset_sat_high) * sat.item(tuple(reversed(max_loc)))
  value_high_thresh = (1 + offset_val) * value.item(tuple(reversed(max_loc)))
  if sat_high_thresh > 255:
    sat_high_thresh = 255

  #return [(hue_low_thresh, sat_low_thresh, value_low_thresh), (hue_high_thresh, sat_high_thresh, value_high_thresh)]
  return [(hue_low_thresh, sat_low_thresh, 0), (hue_high_thresh, sat_high_thresh, 255)]

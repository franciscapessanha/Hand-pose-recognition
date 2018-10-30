import cv2 as cv
import numpy as np


rectangle_size = 20

def draw_sample_rectangles(frame):
  height, width, _ = frame.shape

  rect1_top = (int(width/2 - rectangle_size/2), int(height*(1/3) - rectangle_size/2))
  rect2_top = (int(width/2 - rectangle_size/2), int(height*(2/3) - rectangle_size/2))

  cv.rectangle(frame,
    rect1_top,
    (rect1_top[0] + rectangle_size, rect1_top[1] + rectangle_size),
    (0,255,0),
    1)

  cv.rectangle(frame,
    rect2_top, 
    (rect2_top[0] + rectangle_size, rect2_top[1] + rectangle_size), 
    (0,255,0),
    1)

def get_samples(frame):
  height, width, _ = frame.shape

  hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
  hsv_frame = cv.medianBlur(hsv_frame,5)

  rect1_top = (int(width/2 - rectangle_size/2), int(height*(1/3) - rectangle_size/2))
  rect2_top = (int(width/2 - rectangle_size/2), int(height*(2/3) - rectangle_size/2))
  rect1 = hsv_frame[rect1_top[1]:rect1_top[1]+rectangle_size, rect1_top[0]:rect1_top[0]+rectangle_size]
  rect2 = hsv_frame[rect2_top[1]:rect2_top[1]+rectangle_size, rect2_top[0]:rect2_top[0]+rectangle_size]

  return [rect1, rect2]

def calculate_sample_values(sample, offset_hue, offset_sat_low, offset_sat_high):
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

  print(hue_low_thresh)
  print(hue_high_thresh)

  print(sat_low_thresh)
  print(sat_high_thresh)

  #return [(hue_low_thresh, sat_low_thresh, value_low_thresh), (hue_high_thresh, sat_high_thresh, value_high_thresh)]
  return [(hue_low_thresh, sat_low_thresh, 0), (hue_high_thresh, sat_high_thresh, 255)]

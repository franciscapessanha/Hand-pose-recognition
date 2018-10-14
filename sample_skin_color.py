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

def calculate_sample_values(sample1, sample2, offset_hue, offset_sat):
  hue1, sat1, _ = cv.split(sample1)
  hue2, sat2, _ = cv.split(sample2)

  min_val1, max_val1, min_loc1, max_loc1 = cv.minMaxLoc(hue1)
  min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(hue2)

  hue_low_thresh = (1 - offset_hue) * min(min_val1, min_val2)
  if hue_low_thresh < 0:
    hue_low_thresh = 0

  hue_high_thresh = (1 + offset_hue) * max(max_val1, max_val2) 
  if hue_high_thresh > 180:
    hue_high_thresh = 180
  
  if min_val1 <= min_val2:
    sat_low_thresh = (1 - offset_sat) * sat1[min_loc1]
  else: 
    sat_low_thresh = (1 - offset_sat) * sat2[min_loc2]
  if sat_low_thresh < 0:
    sat_low_thresh = 0

  if max_val1 >= max_val2:
    sat_high_thresh = (1 + offset_sat) * sat1[max_loc1]
  else:
    sat_high_thresh = (1 + offset_sat) * sat2[max_loc2]
  if sat_high_thresh > 255:
    sat_high_thresh = 255

  print('hue_low', hue_low_thresh)
  print('hue_high',hue_high_thresh)
  print('sat_low', sat_low_thresh)
  print('sat_high', sat_high_thresh)

  return [(hue_low_thresh, sat_low_thresh, 0), (hue_high_thresh, sat_high_thresh, 255)]

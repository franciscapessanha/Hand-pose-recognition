import cv2 as cv
import numpy as np

rectangle_size = 20

def draw_sample_rectangles(frame):
  height, width, _ = frame.shape

  rect_1_top = (int(width/2 - rectangle_size/2), int(height*(1/3) - rectangle_size/2))
  rect_2_top = (int(width/2 - rectangle_size/2), int(height*(2/3) - rectangle_size/2))

  cv.rectangle(frame,
    rect_1_top,
    (rect_1_top[0] + rectangle_size, rect_1_top[1] + rectangle_size),
    (0,255,0),
    1)

  cv.rectangle(frame,
    rect_2_top, 
    (rect_2_top[0] + rectangle_size, rect_2_top[1] + rectangle_size), 
    (0,255,0),
    1)

def get_samples(frame):
  height, width, _ = frame.shape

  hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

  rect_1_top = (int(width/2 - rectangle_size/2), int(height*(1/3) - rectangle_size/2))
  rect_2_top = (int(width/2 - rectangle_size/2), int(height*(2/3) - rectangle_size/2))
  rect_1 = hsv_frame[rect_1_top[1]:rect_1_top[1]+rectangle_size, rect_1_top[0]:rect_1_top[0]+rectangle_size]
  rect_2 = hsv_frame[rect_2_top[1]:rect_2_top[1]+rectangle_size, rect_2_top[0]:rect_2_top[0]+rectangle_size]

  return calculate_sample_values(rect_1, rect_2)

def calculate_sample_values(sample1, sample2):

  
  hue1, sat1, _ = cv.split(sample1)
  hue2, sat2, _ = cv.split(sample2)


  min_val1, max_val1, min_loc1, max_loc1 =  cv.minMaxLoc(hue1)
  min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(hue2)

  print('min_val1 ', min_val1)  
  print('min_val2 ', min_val2)

  print('max_val1 ', max_val1)  
  print('max_val2 ', max_val2)

  offset_hue = 0.30
  hLowThreshold = (1-offset_hue)* min(min_val1, min_val2)
  if hLowThreshold < 0: hLowThreshold=0
  hHighThreshold = (1+offset_hue)* max(max_val1, max_val2) 
  if hHighThreshold > 180: hLowThreshold=180
  
  offset_sat = 0.80
  if min(min_val1, min_val2) == min_val1: min_sat = (1-offset_sat)* sat1[min_loc1]
  else: min_sat = (1-offset_sat)*  sat2[min_loc2]
  if min_sat < 0: min_sat=0

  if max(max_val1, max_val2) == max_val1: max_sat = (1+offset_sat)* sat1[max_loc1]
  else: max_sat = (1+offset_sat)* sat2[max_loc2]
  if max_sat > 255: max_sat = 255

  #sLowThreshold = min([min_val1s, max_val2s]) - offsetLowThreshold
  #sHighThreshold = max(max_val1s, max_val2s) + offsetHighThreshold

  print('min_t ', hLowThreshold)  
  print('max_t ', hHighThreshold)
  print('min_s ', min_sat)  
  print('max_s ', max_sat)
  
  

  return [(hLowThreshold, min_sat, 0), (hHighThreshold, max_sat, 255)]
 
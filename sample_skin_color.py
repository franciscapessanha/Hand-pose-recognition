import cv2 as cv

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
  offsetLowThreshold = 30
  offsetHighThreshold = 30

  meanSample1 = cv.mean(sample1)
  meanSample2 = cv.mean(sample2)

  hLowThreshold = min([meanSample1[0], meanSample2[0]]) - offsetLowThreshold
  hHighThreshold = max([meanSample1[0], meanSample2[0]]) + offsetHighThreshold

  sLowThreshold = min([meanSample1[1], meanSample2[1]]) - offsetLowThreshold
  sHighThreshold = max([meanSample1[1], meanSample2[1]]) + offsetHighThreshold

  return [(hLowThreshold, sLowThreshold, 0), (hHighThreshold, sHighThreshold, 255)]

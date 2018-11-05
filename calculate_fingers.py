import cv2 as cv
import numpy as np
import math
from calculate_contours import get_contours, draw_contours
from calculate_convex_hull import get_convex_hulls, draw_hulls_and_vertices,calculate_convexity_defects
from numpy import linalg

def get_fingers(mask, frame): 
  '''Returns a copy of the original frame and the text to be display in the frame
  
  Arguments:
    mask {Mat} -- Filtered and croped binary mask from a given frame
    frame {Mat} --  Original frame
  
  Returns:
    Mat -- Copy of the original frame
    String - Number of digits/type gesture displayed on the frame 
  '''

  frame_copy = np.copy(frame)
  contours, orientations = get_contours(mask)
  draw_contours(frame_copy, contours)
  hulls, clustered_hulls_vertices = get_convex_hulls(contours)
  #draw_hulls_and_vertices(frame_copy,hulls,clustered_hulls_vertices)
  contours_with_defects = calculate_convexity_defects(contours, clustered_hulls_vertices)
  count_fingers_list = draw_defects(frame_copy, contours_with_defects, mask,contours, orientations)
  text = identify_fingers(count_fingers_list, orientations)

  return frame_copy, text

def draw_defects(frame, contours_with_defects, mask,contours, orientations):
  '''Returns the number of fingers of each hand after filtering the convexity defects.
  Shows the detected fingertips on the original frame
  
  Arguments:
    frame {Mat} -- Frame where the defects are from
    contours_with_defects {List} -- List of convexity defects
    mask {Mat} -- Filtered and croped binary hand mask from a given frame
    contours {List} -- List of contours from mask
    orientation {List} -- composed by 3 elements: vertical/horizontal orientation (boolean), fingers direction (boolean) and
      an array ([x,w,y,h]) of x and y coordinates of top-left border, width and height of the hand 
  
  Returns:
    List -- Number of fingers of each hand present on the original frame
  '''

  count_fingers_list = []
  for contour_with_defects, contour, orientation in zip(contours_with_defects, contours, orientations):
    c = np.asarray(np.vstack(contour_with_defects))
    M = cv.moments(c)
    centroid_x = int(M['m10'] / M['m00'])
    centroid_y = int(M['m01'] / M['m00'])

    x, y, w, h= cv.boundingRect(contour)
    orientation.append("vertical" if h > w else "horizontal") #true if the cropped mask is vertical
    orientation.append([x,w,y,h])

    count_fingers = 0

    '''
    # To draw, on the original frame, the lines that unite the convexity defects
    for new_triple in contour_with_defects:
      # blue lines - contour with defects
      cv.line(frame_copy,tuple(new_triple[0]),tuple(new_triple[1]),[255,0,0],2)
      cv.line(frame_copy,tuple(new_triple[1]),tuple(new_triple[2]),[255,0,0],2)
    '''
    for i in range(len(contour_with_defects)): 
      triple1 = contour_with_defects[i]
      triple2 = contour_with_defects[i - 1]
      new_triple = [triple1[1], triple2[2], triple2[1]]

      if check_mask_cutoff(triple1, triple2):
        continue
      #cv.circle(frame,tuple(new_triple[1]), 5, [0, 0, 255], 3)
      if filter_vertices_by_angle(new_triple, 90) and filter_vertices_by_distance([centroid_x,centroid_y], new_triple[1],orientation):
          cv.circle(frame,tuple(new_triple[1]), 8, [0, 0, 255], 3)

          '''
          # To show the convexity defects on the original frame
          cv.circle(frame_copy,tuple(new_triple[0]),8,[0,255,0],3)
          cv.circle(frame_copy,tuple(new_triple[2]),10,[255,0,0],3)
          '''
          count_fingers += 1 #analisar o interior  -verificar se pertence à mascara

    count_fingers_list.append(count_fingers)

  return count_fingers_list

def check_mask_cutoff(triple1, triple2):
  '''Checks if the connection of the 2 triples occurs when the mask is cut off at wrist
  
  Arguments:
    triple1 {List} -- Points for first triple to be tested
    triple2 {List} -- Points for second triple to be tested
  
  Returns:
    Boolean -- If the two triples are at the mask wrist cut
  '''

  return (triple1[0][0] == triple2[2][0] and abs(triple1[0][1] - triple2[2][1]) > 60 or
    triple1[0][1] == triple2[2][1] and abs(triple1[0][0] - triple2[2][0]) > 60)

def filter_vertices_by_angle(triple, max_angle):
  '''Returns True if the angle between the conevexity defects is lower than the defined maximum angle 
  
  Arguments:
    
    triple {List} -- Composed by arrays w/ dimension (1,3) and each one is coordinates of the convexity defects group 
    max_angle {Integer} -- Maximum angle that can be formed by the three triple's points 
  
  Returns:
    Boolean -- True if the angle is lower than the max_angle
  '''
  a = linalg.norm(triple[0] - triple[2])
  b = linalg.norm(triple[1] - triple[2])
  c = linalg.norm(triple[1] - triple[0])
  angle = np.arccos(((b ** 2 + c ** 2 - a ** 2) /(2 * b * c))) * (180 / np.pi)
  return angle < max_angle

def calculate_distance(pt0, pt1):
  '''Returns the eucledian distance between the points pt0 and pt1

  Arguments:
    pt0 {List} -- Coordinates of the point pt0
    pt1 {List} -- Coordinates of the point pt1
    
  Returns:
    Float -- eucledian distance between the points pt0 and pt1
  '''
  return math.sqrt((pt0[0] - pt1[0]) ** 2 + (pt0[1] - pt1[1]) ** 2)

def filter_vertices_by_distance(pt0, pt1, orientation):
  '''Returns True if the distance between the hand's centroid and hand's fingertip is acceptable within a defined range
  
  Arguments:
    pt0 {List} -- Coordinates of the centroid of the cropped hand
    pt1 {List} -- Coordinates of the detected fingertip of the cropped hand
    orientation {List} -- composed by 3 elements: vertical/horizontal orientation (boolean), fingers direction (boolean)and 
      an array ([x,w,y,h]) of x and y coordinates of top-left border, width and height of the hand 
  
  Returns:
    Boolean -- True if the distance between the hand's centroid and fingertip is valid
  '''
  dist_max_offset = 0.55
  distance = None

  if "vertical" in orientation:
    if "up" in orientation: #vertical image with finger on the top border
      dist_max = max(abs(calculate_distance(pt0, [orientation[-1][0], orientation[-1][2]])), abs(calculate_distance(pt0, [orientation[-1][0] + orientation[-1][1], orientation[-1][2]])))
      distance = calculate_distance(pt0, pt1)

      if pt0[1] + orientation[-1][3] / 8 - pt1[1] < 0: # centroid (x0, y0 + w/10)
        distance = 0
      else:
        distance = calculate_distance(pt0, pt1)
  
    elif "down" in orientation: #vertical image with finger on the bottom border
      dist_max = max(abs(calculate_distance(pt0, [orientation[-1][0], orientation[-1][2] + orientation[-1][3]])), abs(calculate_distance(pt0, [orientation[-1][0] + orientation[-1][1], orientation[-1][2] + orientation[-1][3]])))
      distance = calculate_distance(pt0, pt1)
      
      if pt0[1] - orientation[-1][3] / 8 - pt1[1] > 0: # centroid (x0, y0 - w/10)
        distance = 0
      else:
        distance = calculate_distance(pt0, pt1)
    
  elif "horizontal" in orientation:
    if "right" in orientation: #horizontal image with finger pointing right
      dist_max = max(abs(calculate_distance(pt0, [orientation[-1][0] + orientation[-1][1], orientation[-1][2]])), abs(calculate_distance(pt0, [orientation[-1][0] + orientation[-1][1], orientation[-1][2] + orientation[-1][3]])))
      distance = calculate_distance(pt0, pt1)
      
      if pt0[0] - (orientation[-1][1]) / 8 - pt1[0] > 0:
        distance = 0
      else:
        distance = calculate_distance(pt0, pt1)
        
    elif "left" in orientation: #horizontal image with finger pointing left
      dist_max = max(abs(calculate_distance(pt0, [orientation[-1][0], orientation[-1][2]])), abs(calculate_distance(pt0, [orientation[-1][0], orientation[-1][2] + orientation[-1][3]])))
      distance = calculate_distance(pt0, pt1)
      
      if pt0[0] + (orientation[-1][1] / 8) - pt1[0] < 0: 
        distance = 0
      else:
        distance = calculate_distance(pt0, pt1)

  if distance is None:
    print("Sampling error")
    distance = -1
    dist_max = 0    
  return distance > dist_max_offset * dist_max

def identify_fingers(count_fingers_list, orientations):
  '''Returns the text displayed on the bottom of the original frame
  
  Arguments:
    
    count_fingers {List} --  Number of fingers of each hand
    orientations {List} -- composed by 3 elements: vertical/horizontal orientation (boolean), fingers direction (boolean)and 
      an array ([x,w,y,h]) of x and y coordinates of top-left border, width and height of the hand 
  
  Returns:
    String -- Number of fingers/hand gesture of each hand present on the original frame
  '''
  text = []
  hand_count_list = []

  for count_fingers, orientation in zip(count_fingers_list, orientations):
    hand_gesture = ''
    ratio_width_height = orientation[-1][1] / orientation[-1][3] # width/height
    if count_fingers == 1:
      if (ratio_width_height > 0.65 and orientation[-1][3] > orientation[-1][1]) or (ratio_width_height < 1.54 and orientation[-1][1] > orientation[-1][3]):
        text.append('ok')

      elif "vertical" in orientation: #image is vertical
          hand_count_list.append(1)
          text.append(str(count_fingers))
     
      elif "horizontal" in orientation: #image is horizontal
        if "right" in orientation: #pointing right
          text.append('pointing right')
        elif "left" in orientation: #pointing left
          text.append('pointing left')

    elif count_fingers == 3:
      if "vertical" and "up" in orientation: #image is vertical and three fingers up
        if ratio_width_height > 0.65:
          text.append('all right')
        else: #image is vertical and three fingers down
          hand_count_list.append(3)
          text.append(str(count_fingers))
      else: #image is horizontal
        hand_count_list.append(3)
        text.append(str(count_fingers))

    else:
      hand_count_list.append(count_fingers)
      text.append(str(count_fingers))

  text = text[::-1]
  return text


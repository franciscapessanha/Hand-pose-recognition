import cv2 as cv
import numpy as np
import math # to calculate square root
from calculate_contours import get_contours, draw_contours
from calculate_convex_hull import get_convex_hulls, draw_hulls_and_vertices,calculate_convexity_defects
from numpy import linalg

def get_fingers(mask,original_frame): 
  '''Returns a copy of the original frame and the text that will be display in the frame
  
  Arguments:
    mask {Mat} -- Filtered and croped binary mask from a given frame
    frame {Mat} --  Original frame
  
  Returns:
    Mat -- Copy of the original frame
    String - Number of digits/type gesture displayed on the frame 
  '''

  frame_copy = np.copy(original_frame)
  contours,orientation = get_contours(mask)
  print(type(orientation))
  draw_contours(frame_copy,contours)
  hulls, clustered_hulls_vertices = get_convex_hulls(contours)
  #draw_hulls_and_vertices(frame_copy,hulls,clustered_hulls_vertices)
  contours_with_defects = calculate_convexity_defects(contours,clustered_hulls_vertices)
  count_fingers_list = draw_defects(frame_copy,contours_with_defects, mask,orientation)
  text=identify_fingers(count_fingers_list,contours,orientation)

  return frame_copy, text 

def draw_defects(frame_copy, contours_with_defects,mask,orientation): 
  '''Returns the number of fingers of each hand after filtering the convexity defects. 
  Shows the detected fingertips on the original frame
  
  Arguments:
    
    frame_copy {Mat} --  Copy of the original frame
    contours {List} -- List of contours from mask
    mask {Mat} -- Filtered and croped binary hand mask from a given frame
    orientation {List} -- composed by 3 elements: vertical/horizontal orientation (boolean), fingers direction (boolean)and 
      an array ([x,w,y,h]) of x and y coordinates of top-left border, width and height of the hand 
  
  Returns:
    List -- Number of fingers of each hand present on the original frame
  '''

  count_fingers_list = []
  for contour_with_defects,j in zip(contours_with_defects,range(0,len(orientation))):
    c=np.asarray(np.vstack(contour_with_defects))
    M = cv.moments(c)
    centroid_x=int(M['m10']/M['m00'])
    centroid_y=int(M['m01']/M['m00'])
    
    count_fingers = 0

    '''
    # To draw, on the original frame, the lines that unite the convexity defects
    for new_triple in contour_with_defects:
      # blue lines - contour with defects
      cv.line(frame_copy,tuple(new_triple[0]),tuple(new_triple[1]),[255,0,0],2)
      cv.line(frame_copy,tuple(new_triple[1]),tuple(new_triple[2]),[255,0,0],2)
    '''
    for i in range(0,len(contour_with_defects)): 
      triple1 = contour_with_defects[i]
      triple2 = contour_with_defects[i - 1]
      new_triple = [triple1[1], triple2[2], triple2[1]]
      
      if check_mask_cutoff(triple1, triple2):
        cv.circle(frame_copy,tuple(new_triple[1]),3,[0,255,0],3)
        continue

      if filter_vertices_by_angle(new_triple,90):
        if(filter_vertices_by_distance([centroid_x,centroid_y], new_triple[1],orientation[j])):

          cv.circle(frame_copy,tuple(new_triple[1]),5,[0,0,255],3)
          '''
          # To show the convexity defects on the original frame
          cv.circle(frame_copy,tuple(new_triple[0]),8,[0,255,0],3)
          cv.circle(frame_copy,tuple(new_triple[2]),10,[255,0,0],3)
          '''

          count_fingers = count_fingers + 1 #analisar o interior  -verificar se pertence à mascara
    count_fingers_list.append(count_fingers)
   
  return count_fingers_list

def check_mask_cutoff(triple1, triple2):
  '''

  '''
  return (triple1[0][0] == triple2[2][0] and abs(triple1[0][1] - triple2[2][1]) > 60 or
    triple1[0][1] == triple2[2][1] and abs(triple1[0][0] - triple2[2][0]) > 60)

def filter_vertices_by_angle(triple,max_angle):
  '''
  Returns True if the angle between the conevexity defects is lower than the defined maximum angle 
  
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
  
  if angle < max_angle:
    return True

  return False

def identify_fingers(count_fingers_list,contours,mask, clustered_hulls_vertices):
  text = []
  hand_count_list=[]

  for count_fingers, contour, hull in zip(count_fingers_list, contours, clustered_hulls_vertices):
    hand_gesture = ''
    if count_fingers == 1:
      x, y, w, h = cv.boundingRect(contour)
      ratio_width_height = w / h
      if h > w: #image is vertical
        if ratio_width_height > 0.65:
          text.append('ok')
        else:
          hand_count_list.append(1)
          text.append(str(count_fingers))
      else: #image is horizontal
        if ratio_width_height < 1 / 0.65:
           text.append('ok')
        else:
          text.append('pointer')
    
    elif count_fingers == 3:
      x, y, w, h = cv.boundingRect(contour)
      ratio_width_height = w / h
      if h > w: #image is vertical
        if ratio_width_height > 0.65:
          text.append('all right')
        else:
          hand_count_list.append(3)
          text.append(str(count_fingers))
      else: #image is horizontal
        if ratio_width_height < 1 / 0.65:
           text.append('all right')
        else:
          hand_count_list.append(3)
          text.append(str(count_fingers))
   
    else:
      hand_count_list.append(count_fingers)
      text.append(str(count_fingers))
  
  return text

  
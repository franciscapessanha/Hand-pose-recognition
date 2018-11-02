import cv2 as cv
import numpy as np
from calculate_contours import get_contours, draw_contours
from calculate_convex_hull import get_convex_hulls, draw_hulls_and_vertices,calculate_convexity_defects
from numpy import linalg

def get_fingers(mask,original_frame): 
  frame_copy = np.copy(original_frame)
  contours = get_contours(mask) 
  draw_contours(frame_copy,contours)
  hulls, clustered_hulls_vertices = get_convex_hulls(contours, mask)
  draw_hulls_and_vertices(frame_copy,hulls,clustered_hulls_vertices,contours)
  cluster_range=10
  contours_with_defects = calculate_convexity_defects(contours,clustered_hulls_vertices)
  count_fingers_list = draw_defects(frame_copy,contours_with_defects, mask)
  text=identify_fingers(count_fingers_list,contours,mask,clustered_hulls_vertices)
  return frame_copy, text 

def draw_defects(frame_copy, contours_with_defects,mask): #alterar - retirar count_fingers; usar um criterio de área para eliminar o piel inferior
  count_fingers_list = []
  for contour_with_defects in contours_with_defects:
    count_fingers = 0
    for new_triple in contour_with_defects:
      cv.line(frame_copy,tuple(new_triple[0]),tuple(new_triple[1]),[255,0,0],2)
      cv.line(frame_copy,tuple(new_triple[1]),tuple(new_triple[2]),[255,0,0],2)
    for i in range(0,len(contour_with_defects)):
      #cv.circle(frame_copy,tuple(contour_with_defects[i][0]),10,[0,0,255],3)
      triple1 = contour_with_defects[i]
      triple2 = contour_with_defects[i - 1]
      new_triple = [triple1[1], triple2[2], triple2[1]]
      
      if check_frame_edge(triple1, triple2, mask):
        cv.circle(frame_copy,tuple(new_triple[1]),3,[0,255,0],3)
        continue
      if filter_vertices_by_angle(new_triple,60):
        cv.circle(frame_copy,tuple(new_triple[1]),5,[0,0,255],3)
        #cv.circle(frame_copy,tuple(new_triple[0]),8,[0,255,0],3)
        #cv.circle(frame_copy,tuple(new_triple[2]),10,[255,0,0],3)
        count_fingers = count_fingers + 1 #analisar o interior  -verificar se pertence à mascara
    count_fingers_list.append(count_fingers)
  return count_fingers_list

def check_frame_edge(triple1, triple2, frame): #não é a frame é a mask
  distance_from_frame = 5
  return (triple1[0][0] not in range(distance_from_frame, frame.shape[1] - distance_from_frame + 1) or
    triple1[0][1] not in range(distance_from_frame, frame.shape[0] - distance_from_frame + 1) or
    triple2[2][0] not in range(distance_from_frame, frame.shape[1] - distance_from_frame + 1) or
    triple2[2][1] not in range(distance_from_frame, frame.shape[0] - distance_from_frame + 1))

def filter_vertices_by_angle(triple,max_angle):
  a = linalg.norm(triple[0] - triple[2])
  b = linalg.norm(triple[1] - triple[2])
  c = linalg.norm(triple[1] - triple[0])
  angle = np.arccos(((b ** 2 + c ** 2 - a ** 2) /(2 * b * c))) * (180 / np.pi)
  if angle < max_angle:

    return True

  return False

def identify_fingers(count_fingers_list,contours,mask, clustered_hulls_vertices):
  text=[]
  hand_gesture_list=[]
  hand_count_list=[]

  for count_fingers,contour,hull in zip(count_fingers_list,contours,clustered_hulls_vertices):
    hand_gesture=''
    if count_fingers==1:
      x,y,w,h= cv.boundingRect(contour)
      ratio_width_height=w/h
      if h > w: #image is vertical
        if ratio_width_height > 0.65:
          hand_gesture='ok'
        else:
          hand_count_list.append(1)
      if w >= h: #image is horizontal
        if ratio_width_height < 1/0.65:
           hand_gesture='ok'
        else:
          hand_gesture='pointer'
    
    elif count_fingers==3:
      area_hull = cv.contourArea(np.array(hull))
      area_contour = cv.contourArea(np.asarray(contour))
      arearatio= (area_hull - area_contour)/area_contour
      if arearatio > 0.30:
        hand_gesture='all right'
      else:
        hand_count_list.append(3)
      
    else:
      hand_count_list.append(count_fingers)
    
    if hand_gesture: text.append(hand_gesture)

  if hand_count_list: 
    sum_fingers=sum(hand_count_list)
    text.append(str(sum_fingers))

  text.reverse()
  text=' '.join(text)
  return text

def find_circle(mask,frame_copy):
  circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, 20, 200, 50)
  print(circles)
  #if circles is not None:
	  #circles = np.uint8(np.around(circles))
    #for i in circles[0,:]:
      #cv.circle(frame_copy, (i[0], i[1]), i[2],(0,255,0),-1)
  

  
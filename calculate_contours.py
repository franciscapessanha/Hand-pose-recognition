import cv2 as cv
import numpy as np
from numpy import linalg

def get_contours(mask):
  _ , contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv.contourArea, reverse = True) 
  contours = [contours[i] for i in range(len(contours)) if cv.contourArea(contours[i]) > 0.50 * cv.contourArea(contours[0])]
  mask = fill_contours(contours,mask)
  return contours

def fill_contours(contours,mask):
  new_mask = np.zeros(np.asarray(mask).shape, np.uint8)
  for contour in contours:
    np.asarray(contours)
    cv.fillPoly(new_mask, pts =np.asarray(contours), color=(255,255,255))

  return new_mask

def draw_contours(frame_copy, contours):
  cv.drawContours(frame_copy, contours,-1,(0,255,0),2) # green - color for contours 

def bounding_box(contour):
  rect = cv.minAreaRect(contour)
  box = cv.boxPoints(rect)
  box = np.int0(box)
  print(box[0])
  return box

#def crop_min_area_rect(contour, mask):
  #x,y,h,w = cv.boundingRect(contour)
  #box = cv.boxPoints(rect)
  #print(box)

  #mask_crop = img_rot[pts[1][1]:pts[0][1], pts[1][0]:pts[2][0]]

  #cv.imshow("mask crop",mask_crop)

 
  """
  vector_box = ((box[1][1]-box[2][1]),(box[1][0] - box[2][0]))
  print(vector_box)
  vector_border = (mask.shape[1],0)


  angle = np.arccos(np.dot(vector_box,vector_border)/(linalg.norm(vector_border)*linalg.norm(vector_box))) * (180 / np.pi)
  print(angle)

  rows, cols = mask.shape[0] , mask.shape[1]
  M = cv.getRotationMatrix2D((cols/2,rows/2),angle,1)
  rot = cv.warpAffine(mask,M,(cols,rows))
  rot = cv.cvtColor(rot,cv.COLOR_GRAY2BGR)
  cv.drawContours(rot,[box],0,(0,0,255),2)
  cv.drawContours(mask,[box],0,(0,0,255),2)
  
  cv.line(rot,(0,0),(mask.shape[1],0),(255,0,0),3)
  cv.line(rot,(box[0].item(0),box[0].item(1)),(box[1].item(0),box[1].item(1)),(0,255,0),3)

  
  cv.imshow("rotation", rot)
  cv.imshow("mask rotated", mask)
  """

  
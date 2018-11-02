import cv2 as cv
import numpy as np
from numpy import linalg

def get_contours(mask):
  contours = find_contours(mask)
  mask = fill_contours(contours,mask)
  return contours

def find_contours(mask):
  _ , contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv.contourArea, reverse = True) 
  contours = [contours[i] for i in range(len(contours)) if cv.contourArea(contours[i]) > 0.50 * cv.contourArea(contours[0])]
  return contours

def fill_contours(contours,mask):
  new_mask = np.zeros(np.asarray(mask).shape, np.uint8)
  for contour in contours:
    np.asarray(contours)
    cv.fillPoly(new_mask, pts =np.asarray(contours), color=(255,255,255))
  return mask

def draw_contours(frame_copy, contours):
  cv.drawContours(frame_copy, contours,-1,(0,255,0),2) # green - color for contours 
  for contour in contours:
    x,y,w,h= cv.boundingRect(contour)
    #cv.rectangle(frame_copy,(x,y),(x+w,y+h),(0,255,0),2) #desenho bonding box
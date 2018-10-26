import cv2 as cv
import numpy as np
from calculate_convex_hull import get_convex_hull, calculate_convexity_defects

def get_mask(original, values):
  filtered_frame = cv.medianBlur(original, 5)
  hsv_frame = cv.cvtColor(filtered_frame, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_frame, *values)

  mask = cv.medianBlur(mask, 11)
  
  contours, img_contours = calculate_contours(mask)
  mask = fill_contours(contours,mask)
  hulls, clustered_hulls = get_convex_hull(contours, mask)
  
  mask_with_contours = cv.cvtColor(mask,cv.COLOR_GRAY2BGR) 
  contours_with_defects = calculate_convexity_defects(contours, hulls, 10)
  mask_with_contours = draw_contours(original,contours, hulls, clustered_hulls, contours_with_defects)

  return mask_with_contours, mask

def calculate_contours(mask):
  img_contours, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv.contourArea, reverse = True) 
  contours = [contours[i] for i in range(len(contours)) if cv.contourArea(contours[i]) > 0.20 * cv.contourArea(contours[0])]
 
  return contours, img_contours

def fill_contours(contours,mask):
  mask = np.zeros(np.asarray(mask).shape, np.uint8)
  for contour in contours:
    np.asarray(contours)
    cv.fillPoly(mask, pts =np.asarray(contours), color=(255,255,255))

  return mask

def draw_contours(mask,contours, hulls, clustered_hulls, contours_with_defects):
  mask_with_contours = mask.copy()
  cv.drawContours(mask_with_contours, contours,-1,(0,255,0),2) # green - color for contours 

  for i in range(len(contours)):
    color = (0, 0, 255) # red - color for convex hull
    cv.drawContours(mask_with_contours, hulls, i, color, 2, 8)

  for hull in clustered_hulls:
    for point in hull:
      cv.circle(mask_with_contours,(point.item(0), point.item(1)),10,(255,0,0),2)

  for contour_with_defects in contours_with_defects:
    for triple in contour_with_defects:
      cv.circle(mask_with_contours,tuple(triple[1]),5,[0,0,255],-1)
  return mask_with_contours

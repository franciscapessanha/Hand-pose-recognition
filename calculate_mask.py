import cv2 as cv
import numpy as np
from calculate_convex_hull import get_convex_hull, calculate_convexity_defects

def get_mask(original, values):
  #hsv_frame = cv.cvtColor(filtered_frame, cv.COLOR_BGR2HSV)
  adjusted_image = adjust_gamma(original, gamma = 1.5) # reduzir as sombras - torna tudo mais homogeneo
  cv.imshow('after imadjust', adjusted_image)
  filtered_frame = cv.medianBlur(adjusted_image,9)
  
  hsv_frame = cv.cvtColor( filtered_frame, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_frame, *values)
 
  mask, border_size = add_border(mask)
  
  kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))

  close_mask = cv.morphologyEx(mask,cv.MORPH_CLOSE, kernel_ellipse)
  close_mask = cv.medianBlur(mask,3)

  close_mask = close_mask[border_size:-(border_size+1),border_size:-(border_size+1)]

  kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
  dilated_mask = cv.dilate(close_mask,kernel_ellipse, iterations = 2)
  erode_mask = cv.erode(dilated_mask, kernel_ellipse)
  mask = cv.medianBlur(erode_mask, 3)

  #kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
  #filtered_frame = cv.morphologyEx(mask,cv.MORPH_CLOSE,kernel_ellipse)
  
  contours, img_contours = calculate_contours(mask)
  mask = fill_contours(contours,mask)

  hulls, clustered_hulls = get_convex_hull(contours, mask)
  mask_with_contours = cv.cvtColor(mask,cv.COLOR_GRAY2BGR) 
  contours_with_defects = calculate_convexity_defects(contours, hulls, 10)
  mask_with_contours = draw_contours(original,contours, hulls, clustered_hulls, contours_with_defects)

  return mask_with_contours, mask

def adjust_gamma(image, gamma=1.0):
  invGamma = 1.0 / gamma
  table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)])
  return cv.LUT(image.astype(np.uint8), table.astype(np.uint8))

def add_border(image):
  row, col = image.shape[:2]
  bottom = image[row-2:row,0:col]
  mean=cv.mean(bottom)[0]
  border_size = 10
  image=cv.copyMakeBorder(image, top=border_size, bottom=border_size, left=border_size, right=border_size, borderType= cv.BORDER_CONSTANT, value=255)

  return image, border_size
def calculate_contours(mask):
  img_contours, contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv.contourArea, reverse = True) 
  contours = [contours[i] for i in range(len(contours)) if cv.contourArea(contours[i]) > 0.50 * cv.contourArea(contours[0])]
 
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

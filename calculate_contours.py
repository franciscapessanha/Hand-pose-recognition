import cv2 as cv
import numpy as np
from numpy import linalg

def get_contours(mask):
  '''Returns the contours for a given mask after applying a fill and crop to said mask
  
  Arguments:
    mask {Mat} -- Binary mask to calculate contours
  
  Returns:
    List -- List with all the sorted contours from the mask
  '''

  contours = find_contours(mask)
  mask = fill_contours(contours, mask)
  mask,orientation = crop_mask(contours, mask)
  contours = find_contours(mask)
  contours=sort_contours(contours)
  mask = fill_contours(contours, mask)
  return contours,orientation

def find_contours(mask):
  '''Returns all contours for a given mask that are bigger then 50% of the biggest contour, sorted by size
  
  Arguments:
    mask {Mat} -- Binary mask to calculate contours
  
  Returns:
    List -- List with all the contours from the mask
  '''

  _ , contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv.contourArea, reverse = True) 
  contours = [contours[i] for i in range(len(contours)) if cv.contourArea(contours[i]) > 0.50 * cv.contourArea(contours[0])]

  return contours

def fill_contours(contours, mask):
  '''Fills all contours from a mask
  
  Arguments:
    contours {List} -- List of contours to fill
    mask {Mat} -- Binary mask to be filled
  
  Returns:
    Mat -- Mask with filled contours
  '''

  new_mask = np.zeros(np.asarray(mask).shape, np.uint8)
  for contour in contours:
    np.asarray(contours)
    cv.fillPoly(new_mask, pts = np.asarray(contours), color=(255,255,255))
  return new_mask

def draw_contours(frame, contours):
  '''Draws contours in green in a given frame
  
  Arguments:
    frame {Mat} -- Frame to draw in
    contours {List} -- List of contours to draw
  '''

  cv.drawContours(frame, contours,-1,(0,255,0),2) # green - color for contours 

def crop_mask(contours, mask):
  '''Crops a hand mask by the wrist
  
  Arguments:
    contours {List} -- List of contours from mask
    mask {Mat} -- Binary hand mask
  
  Returns:
    Mat -- Mask with cropped wrist and arm
    List -- finger_orientation is a list of booleans:
      True if fingers up or pointing right), False if finger down or pointing left
  '''
  finger_orientation=[]
  for contour in contours:
    x,y,w,h= cv.boundingRect(contour)
    cropped_mask = mask[y:y+h,x:x+w]
    
    if h > w: #image is vertical
      if y == 0: right_side_up = False
      else: right_side_up = True
      vertical_cropped_mask = crop_vertical_mask(cropped_mask, right_side_up)
      if vertical_cropped_mask is None:
        return mask
      mask[y:y+h,x:x+w] = vertical_cropped_mask
      finger_orientation.append([right_side_up])
    
    if w >= h: #image is horizontal
      if x == 0: pointing_right = True
      else: pointing_right = False
      horizontal_cropped_mask = crop_horizontal_mask(cropped_mask, pointing_right)
      if horizontal_cropped_mask is None:
        return mask
      mask[y:y+h,x:x+w] = horizontal_cropped_mask
      finger_orientation.append([pointing_right]) 
  return mask, finger_orientation

def crop_vertical_mask(mask, right_side_up):
  '''Crops a hand mask by the wrist, where the hand is vertical
  
  Arguments:
    mask {Mat} -- Binary hand mask
    right_side_up {Boolean} -- If hand is pointing upward
  
  Returns:
    Mat -- Mask with cropped wrist and arm
  '''

  mask_row_sum = np.sum(mask, axis = 1)
  if right_side_up:
    bottom_to_top = list(reversed(mask_row_sum))
    for i in range(0, len(bottom_to_top) - 20):
      if bottom_to_top[i + 20] > 1.05 * bottom_to_top[i]: # If finds transition
        index_in_mask = mask.shape[0] - i
        non_zero_indexes = np.argwhere(mask[index_in_mask - 1, :]) # Removes all mask points below transition
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for x in range(np.int(first), np.int(last)):
          mask[index_in_mask - 1, x] = 1
        mask[index_in_mask:mask.shape[0], 0:mask.shape[1]] = 0
        return mask
  else:
    top_to_bottom = mask_row_sum
    for i in range(0,len(top_to_bottom) - 20):
      if top_to_bottom[i + 20] > 1.05 * top_to_bottom[i]: # If finds transition
        index_in_mask = i
        non_zero_indexes = np.argwhere(mask[index_in_mask - 1, :]) # Removes all mask points below transition
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for x in range(np.int(first), np.int(last)):
          mask[index_in_mask - 1, x] = 1
        mask[0:index_in_mask, 0:mask.shape[1]] = 0
        return mask


def crop_horizontal_mask(mask, pointing_right):
  '''Crops a hand mask by the wrist, where the hand is horizontal
  
  Arguments:
    mask {Mat} -- Binary hand mask
    pointing_right {Boolean} -- If hand is pointing right
  
  Returns:
    Mat -- Mask with cropped wrist and arm
  '''
  mask_col_sum = np.sum(mask,axis=0)
  if pointing_right:
    left_to_right = mask_col_sum 
    for i in range(0,len(left_to_right)-20):
      if left_to_right[i+20] > 1.05*left_to_right[i]:
        index_in_mask = i
        non_zero_indexes = np.argwhere(mask[:,index_in_mask-1])
        first  = non_zero_indexes[0]
        last  = non_zero_indexes[-1]
        for y in range(np.int(first),np.int(last)):
          mask[y,index_in_mask-1] = 1
        mask[0:mask.shape[0],0:index_in_mask] = 0
        return mask
  else:
    right_to_left = list(reversed(mask_col_sum))
    for i in range(0,len(right_to_left)-20):
      if right_to_left[i+20] > 1.05*right_to_left[i]:
        index_in_mask = mask.shape[1]-i
        non_zero_indexes = np.argwhere(mask[:,index_in_mask-1])
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for y in range(np.int(first),np.int(last)):
          mask[y,index_in_mask-1] = 1
        mask[0:mask.shape[0],index_in_mask:mask.shape[1]] = 0
        return mask

def sort_contours(contours, method=True):
  '''Returns the contours sorted from top to bottom/left to right or from bottom to top/right to left depending if
  the method is True or False,respectively
  
  Arguments:
    contours {List} -- List with all the unsorted contours 
  
  Returns:
    List -- List with all the sorted contours 
  '''
  # initialize the reverse flag and sort index
  i = 0

  if method == False: i = 1

  boundingBoxes = [cv.boundingRect(contour) for contour in contours]
  (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda b:b[1][i], reverse=method))

  return contours
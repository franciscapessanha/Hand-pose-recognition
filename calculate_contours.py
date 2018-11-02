import cv2 as cv
import numpy as np
from numpy import linalg

def get_contours(mask):
  contours = find_contours(mask)
  mask = fill_contours(contours,mask)
  mask = crop_mask(contours, mask)
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

def crop_mask(contours, mask):
  for contour in contours:
    x,y,w,h= cv.boundingRect(contour)
    cropped_mask = mask[y:y+h,x:x+w]
    
    if h > w: #image is vertical
      if y == 0: right_side_up = False
      else: right_side_up = True
      mask[y:y+h,x:x+w] = crop_vertical_mask(cropped_mask,right_side_up)  
    
    if w >= h: #image is horizontal
      if x == 0: pointing_right = True
      else: pointing_right = False
      mask[y:y+h,x:x+w] = crop_horizontal_mask(cropped_mask,pointing_right)

  return mask
    
##deve haver uma forma mais compacta de fazer isto 

def crop_vertical_mask(mask,right_side_up): #fecha o contorno inferiormente
  mask_row_sum = np.sum(mask,axis=1)
  if right_side_up:
    bottom_to_top = list(reversed(mask_row_sum))
    for i in range(0,len(bottom_to_top)-20):
      if bottom_to_top[i+20] > 1.05*bottom_to_top[i]: #se o de cima for muito maior que o debaixo temos uma transição
        index_in_mask = mask.shape[0]-i
        non_zero_indexes = np.argwhere(mask[index_in_mask-1,:]) #o index in mask vai ser removido abaixo
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for x in range(np.int(first),np.int(last)):
          mask[index_in_mask-1,x] = 255
        mask[index_in_mask:mask.shape[0],0:mask.shape[1]] = 0
        return mask
  else:
    top_to_bottom = mask_row_sum
    for i in range(0,len(top_to_bottom)-20):
      if top_to_bottom[i+20] > 1.05*top_to_bottom[i]:  #se  o de cima for muito maior que o debaixo temos uma transição
        index_in_mask = i
        non_zero_indexes = np.argwhere(mask[index_in_mask-1,:])  #o  index in mask vai ser removido abaixo
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for x in range(np.int(first),np.int(last)):
          mask[index_in_mask-1,x] = 255
        mask[0:index_in_mask,0:mask.shape[1]] = 0
        return mask


def crop_horizontal_mask(mask,pointing_right):  #fecha  o contorno inferiormente
  mask_col_sum = np.sum(mask,axis=0)
  if pointing_right:
    left_to_right = mask_col_sum 
    for i in range(0,len(left_to_right)-20):
      if left_to_right[i+20] > 1.05*left_to_right[i]:  #se  o de cima for muito maior que o debaixo temos uma transição
        index_in_mask = i
        non_zero_indexes = np.argwhere(mask[:,index_in_mask-1])  #o  index in mask vai ser removido abaixo
        first  = non_zero_indexes[0]
        last  = non_zero_indexes[-1]
        for y in range(np.int(first),np.int(last)):
          mask[y,index_in_mask-1] = 255
        mask[0:mask.shape[0],0:index_in_mask] = 0
        return mask
  else:
    right_to_left = list(reversed(mask_col_sum))
    for i in range(0,len(right_to_left)-20):
      if right_to_left[i+20] > 1.05*right_to_left[i]:  #se  o de cima for muito maior que o debaixo temos uma transição
        index_in_mask = mask.shape[1]-i
        non_zero_indexes = np.argwhere(mask[:,index_in_mask-1])  #o  index in mask vai ser removido abaixo
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for y in range(np.int(first),np.int(last)):
          mask[y,index_in_mask-1] = 255
        mask[0:mask.shape[0],index_in_mask:mask.shape[1]] = 0
        return mask

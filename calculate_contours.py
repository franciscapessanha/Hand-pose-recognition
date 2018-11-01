import cv2 as cv
import numpy as np
from numpy import linalg

def get_contours(mask):
  contours = find_contours(mask)
  mask = crop_mask (contours, mask)
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
    mask = crop_mask(contours, mask)

  return new_mask

def draw_contours(frame_copy, contours):
  cv.drawContours(frame_copy, contours,-1,(0,255,0),2) # green - color for contours 
    

def crop_mask(contours, mask):
  for contour in contours:
    x,y,w,h= cv.boundingRect(contour)
    if h > w: #image is vertical
      mask = crop_vertical_mask(mask)
    else:
      mask = crop_horizontal_mask(mask)

  return mask

def crop_vertical_mask(mask): #fecha o contorno inferiormente
  mask_row_sum = np.sum(mask,axis=1)
  bottom_to_top = list(reversed(mask_row_sum))
  for i in range(0,len(bottom_to_top)-20):
      if bottom_to_top[i+20] > 1.1*bottom_to_top[i]: #se o de cima for muito maior que o debaixo temos uma transição
        index_in_mask = mask.shape[0]-i
        non_zero_indexes = np.argwhere(mask[index_in_mask-1]) #o index in mask vai ser removido abaixo
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for x in range(np.int(first),np.int(last)):
          mask[index_in_mask-1][x] = 255
        
        mask = mask[0:index_in_mask,0:mask.shape[1]]
        return mask
        
def crop_horizontal_mask(mask): #fecha o contorno inferiormente
  mask_col_sum = np.sum(mask,axis=0)
  mask_col_sum = list(reversed(mask_col_sum))
  print(mask_col_sum)
  for i in range(0,len(mask_col_sum)-20):
      if mask_col_sum[i+20] > 1.1*mask_col_sum[i]: #se o de cima for muito maior que o debaixo temos uma transição
        index_in_mask = shape[1]-i
        non_zero_indexes = np.argwhere(mask[:][i]) #o index in mask vai ser removido abaixo
        first = non_zero_indexes[0]
        last = non_zero_indexes[-1]
        for x in range(np.int(first),np.int(last)):
          mask[y][index_in_mask-1] = 255
        
        mask = mask[0:mask.shape[0],0:index_in_mask]
        return mask


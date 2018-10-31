import cv2 as cv
import numpy as np

def get_mask(original_frame, values):
  filtered_frame = filter_frame(original_frame)
  hsv_frame = cv.cvtColor( filtered_frame, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_frame, *values)
  mask = get_vertical_projection(mask)
  mask = filter_mask(mask)
  cv.imshow("final mask", mask)
  return mask

def filter_frame(original_frame):
  adjusted_frame = adjust_gamma(original_frame, gamma = 1.5) # reduzir as sombras - torna tudo mais homogeneo
  filtered_frame = cv.medianBlur(adjusted_frame,9)
  return filtered_frame

def filter_mask(mask):
  kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
  mask = cv.morphologyEx(mask,cv.MORPH_CLOSE, kernel_ellipse)
  mask = cv.medianBlur(mask,9)
  mask = cv.dilate(mask,kernel_ellipse, iterations = 2)
  mask = cv.medianBlur(mask, 9)
  return mask

def adjust_gamma(image, gamma=1.0):
  invGamma = 1.0 / gamma
  table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)])
  return cv.LUT(image.astype(np.uint8), table.astype(np.uint8))

def get_vertical_projection(mask): #fecha o contorno inferiormente
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


  

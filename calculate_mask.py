import cv2 as cv
import numpy as np
from calculate_contours import get_contours, fill_contours, draw_contours

def get_mask(original_frame, values): #shadow removal: devem ser regiões com uma hue and sat proxima mas uma intensidsde muito mais baixa (HSI) - tentava fazer a correção na intensidade. uniformizar intensidade 
  hsv_frame = cv.cvtColor( original_frame, cv.COLOR_BGR2HSV)
  filtered_frame = filter_frame(hsv_frame, original_frame)
  mask = cv.inRange(hsv_frame, *values)
  mask = filter_mask(mask)
  cv.imshow("final mask", mask)
  return mask

def filter_frame(hsv_frame, original_frame):
  #adjusted_frame = adjust_gamma(original_frame, gamma = 1.5) # reduzir as sombras - torna tudo mais homogeneo
  h, s, _ = cv.split(hsv_frame)
  b, g, r = cv.split(original_frame)
  i = np.divide(b+g+r,3)
  i = np.uint8(i)
  filtered_frame = cv.merge((h, s, i))
  cv.imshow("hsi", filtered_frame)
  filtered_frame = cv.medianBlur(filtered_frame,5)
  return filtered_frame

def filter_mask(mask): #projeção vertical para eliminar o braço -deve ser a primeira transição grande. orientação da mão a partir das linhas dos dedos e fazer uma rotação em relação a isso
  mask, border_size = add_border(mask)
  kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5)) #por vezes funde em cima (centrar mão)
  mask = cv.morphologyEx(mask,cv.MORPH_CLOSE, kernel_ellipse)
  mask = cv.medianBlur(mask,5)

  mask = mask[border_size:-(border_size+1),border_size:-(border_size+1)] #remove border

  mask = cv.dilate(mask, kernel_ellipse, iterations=2)
  mask = cv.erode(mask, kernel_ellipse, iterations=2)
  mask = cv.medianBlur(mask, 5)

  return mask

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
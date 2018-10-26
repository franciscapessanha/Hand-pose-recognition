import cv2 as cv
import numpy as np
from sklearn.cluster import DBSCAN

def get_convex_hull(contours,img):
  hulls = [cv.convexHull(contour,False) for contour in contours]
  clustered_hulls = calculate_clustered_hulls(hulls, 20)
  
  return hulls, clustered_hulls

def calculate_clustered_hulls(hulls, radius): #alterar nome
  clustered_hulls = []
  for hull in hulls:
    points = np.array([[point.item(0), point.item(1)] for point in hull]) # converts hull to np array
    clustering = DBSCAN(eps=radius, min_samples=1).fit(points)
    clusters = [points[clustering.labels_ == i] for i in range(len(set(clustering.labels_)))]
    clustered_hulls.append([np.mean(cluster, axis=0).astype(int) for cluster in clusters])
  return clustered_hulls

def calculate_convexity_defects(contours, mask_with_contours):
  for contour in contours:
    hull = cv.convexHull(contour, returnPoints = False)
    defects = cv.convexityDefects(contour, hull)
    for i in range(defects.shape[0]):
      _,_,f,_ = defects[i,0]
      far = tuple(contour[f][0])
      cv.circle(mask_with_contours,far,5,[0,0,255],-1)
pass
  
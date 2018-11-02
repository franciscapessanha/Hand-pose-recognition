import cv2 as cv
import numpy as np
from sklearn.cluster import DBSCAN

def get_convex_hulls(contours,frame_copy):
  hulls = [cv.convexHull(contour,False) for contour in contours]
  clustered_hulls_vertices = cluster_hulls_vertices(hulls, 20)
  return hulls, clustered_hulls_vertices

def cluster_hulls_vertices(hulls, radius): 
  clustered_hulls_vertices = []
  for hull in hulls:
    points = np.array([[point.item(0), point.item(1)] for point in hull]) # converts hull to np array
    clustering = DBSCAN(eps=radius, min_samples=1).fit(points)
    clusters = [points[clustering.labels_ == i] for i in range(len(set(clustering.labels_)))]
    mean_point_cluster = []
    for cluster in clusters:
      best_point, min_dist = 0, 9999
      mean_point = np.mean(cluster, axis=0).astype(int)
      for point in cluster:
        dist = np.linalg.norm(point - mean_point)
        if dist < min_dist:
          best_point = point
          min_dist = dist
      mean_point_cluster.append(best_point)
    clustered_hulls_vertices.append(mean_point_cluster)
  return clustered_hulls_vertices

def get_indexed_hull(contour, hull):
  indexed_hull = []
  for hull_point in hull:
    for index, contour_point in enumerate(contour):
      if contour_point[0][0] == hull_point[0] and contour_point[0][1] == hull_point[1]:
        indexed_hull.append(index)

  return np.array(indexed_hull)

def calculate_convexity_defects(contours, clustered_hulls_vertices):
  contours_with_defects = []
  for contour, clustered_hull in zip(contours, clustered_hulls_vertices):
    contour_with_defects = []
    hull = cv.convexHull(contour, returnPoints = False)

    indexed_hull = get_indexed_hull(contour, clustered_hull)

    defects = cv.convexityDefects(contour, indexed_hull)
    if defects is None:
      continue
    for i in range(defects.shape[0]):
      s,e,f,_= defects[i,0]
      start = contour[s][0]
      end = contour[e][0]
      defect_point = contour[f][0]
      contour_with_defects.append([start, defect_point, end])

    contours_with_defects.append(contour_with_defects)
  return contours_with_defects

def draw_hulls_and_vertices(frame_copy,hulls,clustered_hulls_vertices,contours):
  for i in range(len(contours)):
    color = (0, 0, 255) # red - color for convex hull
    #cv.drawContours(frame_copy, hulls, i, color, 2, 8)
  
  #for hull in clustered_hulls_vertices:
    #for point in hull:
      #cv.circle(frame_copy,(point.item(0), point.item(1)),2,(255,0,0),2)

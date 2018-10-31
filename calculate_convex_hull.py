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
        dist = np.linalg.norm(point-mean_point)
        if dist < min_dist:
          best_point = mean_point
          min_dist = dist
      mean_point_cluster.append(best_point)
    clustered_hulls_vertices.append(mean_point_cluster)
  return clustered_hulls_vertices

def get_point_in_range(point, hull, cluster_range):
  in_range = False
  closest_hull_point = None
  for hull_point in hull:
    if np.linalg.norm(hull_point-point) < cluster_range:
      in_range = True
      closest_hull_point = hull_point
      break
  return in_range, closest_hull_point

def calculate_convexity_defects(contours, clustered_hulls_vertices, cluster_range):
  contours_with_defects = []
  for contour, clustered_hull in zip(contours, clustered_hulls_vertices):
    contour_with_defects = []
    hull = cv.convexHull(contour, returnPoints = False)
    defects = cv.convexityDefects(contour, hull)
    if defects is None:
      continue
    for i in range(defects.shape[0]):
      s,e,f,_= defects[i,0]

      start = contour[s][0]
      end = contour[e][0]
      defect_point = contour[f][0]
      in_range, _ = get_point_in_range(defect_point, clustered_hull, cluster_range)
      if not in_range:
        start_in_range, start_in_hull = get_point_in_range(start, clustered_hull, cluster_range)
        if not start_in_range:
          start_in_hull = start

        end_in_range, end_in_hull = get_point_in_range(end, clustered_hull, cluster_range)
        if not end_in_range:
          end_in_hull = end

        contour_with_defects.append([np.array(start_in_hull).flatten(), np.array(defect_point).flatten(), np.array(end_in_hull).flatten()])
    contours_with_defects.append(contour_with_defects)
  return contours_with_defects

def draw_hulls_and_vertices(frame_copy,hulls,clustered_hulls_vertices,contours):
  for i in range(len(contours)):
    color = (0, 0, 255) # red - color for convex hull
    cv.drawContours(frame_copy, hulls, i, color, 2, 8)
  
  #for hull in clustered_hulls_vertices:
    #for point in hull:
      #cv.circle(frame_copy,(point.item(0), point.item(1)),2,(255,0,0),2)

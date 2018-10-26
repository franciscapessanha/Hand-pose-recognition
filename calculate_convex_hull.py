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
    clustered_hulls.append(mean_point_cluster)
  return clustered_hulls

def calculate_convexity_defects(contours, clustered_hulls, mask_with_contours, cluster_range):
  contours_with_defects = []
  for contour, clustered_hull in zip(contours, clustered_hulls):
    contour_with_defects = []
    hull = cv.convexHull(contour, returnPoints = False)
    defects = cv.convexityDefects(contour, hull)
    for i in range(defects.shape[0]):
      s,e,f,_ = defects[i,0]
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
        cv.circle(mask_with_contours,tuple(defect_point),5,[0,0,255],-1)

    contours_with_defects.append(contour_with_defects)

    return contours_with_defects

def get_point_in_range(point, hull, cluster_range):
  in_range = False
  closest_hull_point = None
  for hull_point in hull:
    if np.linalg.norm(hull_point-point) < cluster_range:
      in_range = True
      closest_hull_point = hull_point
      break

  return in_range, closest_hull_point
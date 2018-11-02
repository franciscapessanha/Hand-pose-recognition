import cv2 as cv
import numpy as np
from sklearn.cluster import DBSCAN

def get_convex_hulls(contours):
  '''Returns a list of convex hulls for a given list of contours
  
  Arguments:
    contours {List} -- List of contours
  
  Returns:
    List -- List of convex hulls
    List -- List of convex hulls after being clustered
  '''

  hulls = [cv.convexHull(contour, False) for contour in contours]
  clustered_hulls_vertices = cluster_hulls_vertices(hulls, 20)
  return hulls, clustered_hulls_vertices

def cluster_hulls_vertices(hulls, radius):
  '''Clusters a list of hulls vertices using a given radius
  
  Arguments:
    hulls {List} -- List of hulls
    radius {Int} -- Radius for grouping points in cluster
  
  Returns:
    List -- List of hulls with clustered vertices
  '''

  clustered_hulls_vertices = []
  for hull in hulls:
    points = np.array([[point.item(0), point.item(1)] for point in hull]) # converts hull to np array
    clustering = DBSCAN(eps = radius, min_samples = 1).fit(points)
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
  '''Returns a list of indexes corresponding to the points in a contour from a given hull
  
  Arguments:
    contour {List} -- Contour vertices
    hull {List} -- Hull vertices
  
  Returns:
    List -- Indexes of hull vertices in contour list
  '''

  indexed_hull = []
  for hull_point in hull:
    for index, contour_point in enumerate(contour):
      if contour_point[0][0] == hull_point[0] and contour_point[0][1] == hull_point[1]:
        indexed_hull.append(index)

  return np.array(indexed_hull)

def calculate_convexity_defects(contours, hulls):
  '''Returns a list of convexity defects between a list of contours and hulls
  
  Arguments:
    contours {List} -- List of contours
    hulls {Hulls} -- List of hulls
  
  Returns:
    List -- List of convexity defects
  '''

  contours_with_defects = []
  for contour, hull in zip(contours, hulls):
    contour_with_defects = []

    indexed_hull = get_indexed_hull(contour, hull)

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

def draw_hulls_and_vertices(frame, hulls, clustered_hulls):
  '''Draws in frame a line for hulls, and a point in clustered hulls vertices
  
  Arguments:
    frame {Mat} -- Frame to draw in
    hulls {List} -- List of hulls
    clustered_hulls {List} -- List of clustered hulls
  '''

  for i in range(len(hulls)):
    cv.drawContours(frame, hulls, i, (0, 0, 255), 2, 8) # red - color for convex hull

  for hull in clustered_hulls:
    for point in hull:
      cv.circle(frame,(point.item(0), point.item(1)),12,(255,255,0),2) # ligth blue - color for convex hull vertices before convexity defects

import cv2
import numpy as np
from skimage.transform import hough_line_peaks

from auxiliary import find_2dmax


def adapted_hough_line_peaks(hough_arr, angles, rhos, min_rho, min_angle, threshold, show):
  _, found_angles, found_rhos = hough_line_peaks(hough_arr.T,
                                                 angles,
                                                 rhos,
                                                 min_angle=min_angle,
                                                 min_distance=min_rho,
                                                 threshold=threshold)
  if show:
    hough_arr = cv2.cvtColor(np.asarray(hough_arr, dtype=np.float32), cv2.COLOR_GRAY2BGR)

    found_angles_indices = np.apply_along_axis(lambda x: np.where(angles == x), axis=0, arr=found_angles[np.newaxis, :])
    found_rhos_indices = np.apply_along_axis(lambda x: np.where(rhos == x), axis=0, arr=found_rhos[np.newaxis, :])

    for center in zip(found_rhos_indices.squeeze(), found_angles_indices.squeeze()):
      x = int(np.floor(center[0]))
      y = int(np.floor(center[1]))
      cv2.circle(hough_arr, (x, y), 2, (0, 0, 255))

    cv2.namedWindow('houghMaxima', cv2.WINDOW_NORMAL)
    cv2.imshow("houghMaxima", hough_arr)
    cv2.resizeWindow("houghMaxima", 1600, 960)
  return found_rhos, found_angles


def my_hough_peaks(hough_arr, angles, rhos, min_rho, min_angle, threshold, show):
  # angle x rhos
  # rhos[0] - rhos[n] > min_rho
  min_rho_image_span = np.where(rhos - rhos[0] > min_rho)[0][0]
  min_angle_image_span = np.where(angles - angles[0] > min_angle * np.pi / 180)[0][0]
  filter_size = (min_angle_image_span, min_rho_image_span)
  div_point = np.where(rhos > 0)[0][0]
  angle_count = hough_arr.shape[0]
  centers = find_2dmax(hough_arr, filter_size, threshold, mode="reflect", show=show)
  centers = remove_identical_lines(centers, angle_count, div_point, filter_size)
  centers = np.asarray(centers, dtype=int)
  if show:
    hough_arr = cv2.cvtColor(np.asarray(hough_arr, dtype=np.float32), cv2.COLOR_GRAY2BGR)

    for center in centers:
      x = int(np.floor(center[0]))
      y = int(np.floor(center[1]))
      cv2.circle(hough_arr, (x, y), 2, (0, 0, 255))

    cv2.namedWindow('houghMaxima', cv2.WINDOW_NORMAL)
    cv2.imshow("houghMaxima", hough_arr)
    cv2.resizeWindow("houghMaxima", 1600, 960)
  return rhos[centers[:, 0]], angles[centers[:, 1]]


def remove_identical_lines(centers, angle_count, division_point, neighborhood_size):
  if isinstance(neighborhood_size, tuple):
    neighborhood_size_x = neighborhood_size[1]
    neighborhood_size_y = neighborhood_size[0]
  else:
    neighborhood_size_x = neighborhood_size
    neighborhood_size_y = neighborhood_size
  centers_bottom = np.where(centers[:, 1] < angle_count / 2, True, False)
  transformed = np.copy(centers[centers_bottom])
  transformed[:, 1] += angle_count
  transformed[:, 0] = 2 * division_point - transformed[:, 0]
  indices_relative = np.zeros(len(centers[~centers_bottom]))
  # is this possibly somehow broadcastable?
  for point in transformed:
    new_ind = np.where((point[0] - neighborhood_size_x <= centers[~centers_bottom, 0]) &
                       (centers[~centers_bottom, 0] <= point[0] + neighborhood_size_x) &
                       (point[1] - neighborhood_size_y <= centers[~centers_bottom, 1]) &
                       (centers[~centers_bottom, 1] <= point[1] + neighborhood_size_y))
    indices_relative[new_ind] = 1

  try:
    indices_absolute = np.array(np.where(~centers_bottom)).squeeze()[np.where(indices_relative == 1)]
    centers = np.delete(centers, indices_absolute, axis=0)
  except IndexError:
    pass
  return centers

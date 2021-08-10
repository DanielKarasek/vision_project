import cv2
import numpy as np
from scipy.ndimage import convolve as fast_convolve
from scipy.ndimage import label, find_objects
from scipy.ndimage.filters import maximum_filter, minimum_filter


def find_2dmax(inp_arr, filter_size, threshold, mode="reflect", show=False):
  maximum_filtered = maximum_filter(inp_arr, filter_size, mode=mode)
  maxima = (inp_arr == maximum_filtered)

  minimum_filtered = minimum_filter(inp_arr, filter_size, mode=mode)

  if show:
    cv2.imshow("max", maximum_filtered)
    cv2.imshow("min", minimum_filtered)

  diff = ((maximum_filtered - minimum_filtered) > threshold)
  maxima[diff == 0] = 0
  labeled, object_num = label(maxima)

  slices = find_objects(labeled)

  x_centers, y_centers = [], []

  for dy, dx in slices:
    x_centers.append((dx.start + dx.stop - 1) / 2)
    y_centers.append((dy.start + dy.stop - 1) / 2)

  centers = np.array([x_centers, y_centers]).T

  return centers


def sort_lines_by_abs_r(lines_r_angle):
  try:
    indices = np.argsort(np.abs(lines_r_angle[:, 0]), axis=0)
    return lines_r_angle[indices]
  except IndexError:
    return np.array([]), np.array([])


def create_gauss_filter(size, sigma=1):
  """
  Creating gauss filter mat used for convolutions
  :param size: size of filter edge (filter is size x size shaped)
  :param sigma:
  :return: size x size gauss filter
  """
  size = size // 2

  mgrids = np.mgrid[-size:size + 1, -size:size + 1]
  py, px = np.exp(-((mgrids ** 2) / (2.0 * sigma ** 2)))

  g = py * px
  g /= np.sum(g)
  return g


def convolve(img, filter_mat, show=False, convolution_num=0):
  """
  Slow convolution implementation, just for playing around with stuff
  """
  size = filter_mat.shape[0] // 2
  padded = np.pad(img, size, "reflect")
  res = np.copy(img)
  for x in np.arange(img.shape[0]):
    for y in np.arange(img.shape[1]):
      res[x, y] = np.sum(padded[x:x + size * 2 + 1, y:y + size * 2 + 1] * filter_mat)
  if show:
    cv2.imshow("convolved" + str(convolution_num), res)
  return res


def find_intersection(first_line, second_line):
  a = np.cos(first_line[1]) - 1e-12
  b = np.sin(first_line[1]) - 1e-12
  d = np.cos(second_line[1]) - 1e-12
  e = np.sin(second_line[1]) - 1e-12
  c = first_line[0]
  f = second_line[0]
  y = (f - (d * c) / a) / (e - (d * b) / a)
  x = (f - e * y) / d
  return np.floor([x, y])


def contrast_enchantment(img, N, show=False):
  result = np.copy(img)
  NN = N * N
  average_filter = np.ones((N, N)) / NN
  mean = fast_convolve(result, average_filter, mode="nearest")
  std = (fast_convolve(result ** 2, average_filter, mode="nearest") - mean ** 2 + 1e-10)

  D = 0.0002
  result = mean + (D * (result - mean)) / (std + 1e-12)
  np.clip(result, 0, 1)
  cv2.imshow("mean", mean)
  cv2.imshow("std", std)
  if show:
    cv2.imshow("contrast enchancment global", result)
  return result


def find_parallel_pair(lines_r_angle, max_difference):
  pairs = []
  pi_half = np.pi / 2
  for first_line_idx in np.arange(len(lines_r_angle)):
    for second_line_idx in np.arange(first_line_idx + 1, len(lines_r_angle)):
      first_angle = lines_r_angle[first_line_idx][1]
      second_angle = lines_r_angle[second_line_idx][1]
      if np.abs(first_angle - second_angle) > pi_half:
        if first_angle < pi_half:
          first_angle += np.pi
        else:
          second_angle += np.pi
      if (first_angle - max_difference <=
              second_angle <=
              first_angle + max_difference):
        mean_angle = (first_angle + second_angle) / 2
        pairs.append([lines_r_angle[first_line_idx], lines_r_angle[second_line_idx], mean_angle])
  return pairs

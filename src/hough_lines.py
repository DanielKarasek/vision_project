from abc import ABC

import cv2
import numpy as np

from auxiliary import sort_lines_by_abs_r
from line_find_strategies import retrieve_longer_lines
from peak_find_strategies import my_hough_peaks
from sample_strategies import sample_strategy_all


class HoughLines(ABC):
  def __init__(self,
               hough_peaks_fn=my_hough_peaks,
               sample_strategy_fn=sample_strategy_all):
    self.hough_peaks_fn = hough_peaks_fn
    self.sample_strategy_fn = sample_strategy_fn

  def change_hough_peaks_strategy(self, new_hough_peaks_fn):
    self.hough_peaks_fn = new_hough_peaks_fn

  def change_sample_strategy(self, new_sample_fn):
    self.sample_strategy_fn = new_sample_fn


class HoughFullLines(HoughLines):

  def __init__(self,
               hough_peaks_fn=my_hough_peaks,
               sample_strategy_fn=sample_strategy_all,
               retrieve_lines_fn=retrieve_longer_lines):
    super().__init__(hough_peaks_fn=hough_peaks_fn,
                     sample_strategy_fn=sample_strategy_fn)
    self.retrieve_lines_fn = retrieve_lines_fn

  def __call__(self, img, angle_count=960, r_dim=1600, threshold=0.5, min_angle=15, min_rho=15, show=False):
    ys, xs = np.where(img == img.max())

    xs, ys = self.sample_strategy_fn(xs, ys)
    M, N = img.shape

    max_val = np.ceil(np.hypot(M, N))
    min_val = -N

    hough_arr, angles, rhos_image, _ = hough_transform(xs, ys, r_dim, angle_count, min_val, max_val, show=show)
    angles = angles.squeeze()

    found_rhos, found_angles = self.hough_peaks_fn(hough_arr,
                                                   angles,
                                                   rhos_image,
                                                   min_rho,
                                                   min_angle,
                                                   threshold,
                                                   show)
    lines_r_angle = np.array([found_rhos, found_angles]).T
    lines_r_angle = sort_lines_by_abs_r(lines_r_angle)

    lines = self.retrieve_lines_fn(found_rhos, found_angles, N, M)

    return lines, lines_r_angle

  def change_retrieve_lines_strategy(self, new_retrieve_lines_strategy):
    self.retrieve_lines_fn = new_retrieve_lines_strategy


# TODO: make it safe if no segments are found?
class HoughSegments(HoughLines):

  def __call__(self,
               img,
               angle_count=960,
               r_dim=1600,
               threshold=0.5,
               min_angle=15,
               min_rho=15,
               diff_max=6,
               line_width_err=5,
               min_seg_len=40,
               show=False):

    ys, xs = np.where(img == img.max())

    xs, ys = self.sample_strategy_fn(xs, ys)

    M, N = img.shape

    max_val = np.ceil(np.hypot(M, N))
    min_val = -N

    hough_arr, angles, rhos_image, rhos = hough_transform(xs, ys, r_dim, angle_count, min_val, max_val, show=show)

    found_rhos, found_angles = self.hough_peaks_fn(hough_arr,
                                                   angles,
                                                   rhos_image,
                                                   min_rho,
                                                   min_angle,
                                                   threshold,
                                                   show)

    # xs, ys, found_rhos, found_angles, rhos
    segments = []

    line_points = self.prepare_line_points(found_angles, found_rhos)

    angles_indices = np.asarray((angle_count * found_angles - 1) / np.pi, dtype=int)

    for line_num in np.arange(found_rhos.shape[0]):
      responsible_coord_pairs = self.find_responsible_points(xs,
                                                             ys,
                                                             found_rhos,
                                                             angles_indices,
                                                             rhos,
                                                             line_num,
                                                             line_width_err)
      try:
        dists, sorted_coord_pairs = self.get_sorted_dists_coord_pairs(line_points, responsible_coord_pairs, line_num)
        diffs = dists[1:] - dists[:-1]

        segments_idx, segments_idx_shifted = self.get_segment_indices_pairs(diffs, diff_max)
        tmp_segments = self.get_valid_segments(dists, segments_idx_shifted, segments_idx, min_seg_len, sorted_coord_pairs)

        segments.append(tmp_segments)
      except IndexError:
        pass
    segments = np.concatenate(segments)

    if show:
      img_copy = np.copy(img)
      img_copy = cv2.cvtColor(img_copy, cv2.COLOR_GRAY2BGR)

      for segment in segments:
        cv2.line(img_copy, segment[0], segment[1], (0, 255, 0), 3)
      cv2.imshow("segments", img_copy)

    return segments

  @staticmethod
  def prepare_line_points(found_angles, found_rhos):

    angles_sin = np.sin(found_angles)
    angles_cos = np.cos(found_angles)
    xs_0 = angles_cos * found_rhos
    ys_0 = angles_sin * found_rhos

    return np.array([xs_0, ys_0]).T

  @staticmethod
  def find_responsible_points(xs, ys, found_rhos, angles_indices, rhos, line_num, line_width_err):
    rhos_min = found_rhos[line_num] - line_width_err
    rhos_plus = found_rhos[line_num] + line_width_err
    responsible_points = np.where((rhos[:, angles_indices[line_num]] > rhos_min) &
                                  (rhos[:, angles_indices[line_num]] < rhos_plus))[0]

    return np.array([xs[responsible_points], ys[responsible_points]]).T

  @staticmethod
  def get_sorted_dists_coord_pairs(line_points, responsible_coord_pairs, line_num):
    dists = np.sqrt(np.sum(np.abs(line_points[line_num] - responsible_coord_pairs) ** 2, axis=1))
    dists_idx_sorted = np.argsort(dists)
    dists = dists[dists_idx_sorted]
    sorted_coord_pairs = responsible_coord_pairs[dists_idx_sorted]
    return dists, sorted_coord_pairs

  @staticmethod
  def get_segment_indices_pairs(diffs, diff_max):
    segments_idx = np.where(diffs > diff_max)[0]
    segments_idx = np.concatenate([segments_idx, [diffs.shape[0]]])
    segments_idx_shifted = np.roll(segments_idx, 1) + 1
    segments_idx_shifted[0] = 0
    return segments_idx, segments_idx_shifted

  @staticmethod
  def get_valid_segments(dists, segments_idx_shifted, segments_idx, min_seg_len, sorted_coord_pairs):
    seg_lenghts = np.abs(dists[segments_idx_shifted] - dists[segments_idx])
    valid_segs = np.where(seg_lenghts >= min_seg_len)[0]

    tmp_segments = np.array([sorted_coord_pairs[segments_idx_shifted[valid_segs]],
                             sorted_coord_pairs[segments_idx[valid_segs]]])
    tmp_segments = np.swapaxes(tmp_segments, 0, 1)
    return tmp_segments

def hough_transform(xs, ys, r_dim, angle_count, min_val, max_val, show=False):
  hough_trans_arr = np.zeros((angle_count, r_dim))

  angles = np.linspace(0, np.pi, angle_count)
  angles = angles.reshape((1, angle_count))
  xs = np.ascontiguousarray(xs)
  ys = np.ascontiguousarray(ys)
  xs = xs.reshape((xs.shape[0], 1))
  ys = ys.reshape((ys.shape[0], 1))
  rhos = xs * np.cos(angles) + ys * np.sin(angles)
  rhos_image = np.asarray(r_dim * ((np.floor(rhos) - min_val) / (max_val - min_val)),
                          dtype=np.int64)

  counts = get_bincount_along_axis(rhos_image, r_dim, angle_count)

  angles_discrete = np.arange(angle_count)
  hough_trans_arr[angles_discrete, :] = hough_trans_arr[angles_discrete, :] + counts.T
  hough_trans_arr = hough_trans_arr / hough_trans_arr.max()
  if show:
    cv2.namedWindow('hough', cv2.WINDOW_NORMAL)
    cv2.imshow("hough", hough_trans_arr)
    cv2.resizeWindow("hough", 1600, 960)

  return hough_trans_arr, angles.squeeze(), np.linspace(min_val, max_val, r_dim), rhos


def get_bincount_along_axis(rhos_image, r_dim, angle_count):
  result = np.zeros((r_dim, angle_count), dtype=np.int64)
  for column in np.arange(angle_count):
    result[:, column] = np.bincount(rhos_image[:, column], minlength=r_dim)
  return result

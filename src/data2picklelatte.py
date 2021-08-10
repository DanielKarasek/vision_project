from enums import *

from r_score_strategies import *
from line_find_strategies import *
from peak_find_strategies import *
from sample_strategies import *

from copy import deepcopy

# Harris
# Shi_tomasi
# def sample_strategy_all(xs, ys):
# def sample_strategy_every_nth(xs, ys, n):
# def sample_strategy_percentage_rand(xs, ys, percentage):
# def adapted_hough_line_peaks(hough_arr, angles, rhos, min_rho, min_angle, threshold, show):
# def my_hough_peaks(hough_arr, angles, rhos, min_rho, min_angle, threshold, show):
# def retrieve_exact_lines(rhos, angles, N, M):
# def retrieve_longer_lines(rhos, angles, N, M):
# muzu testnout dataclass?


class Database:
  canny_settings = {'sigma': 1}
  nothing_settings = {'sigma': 1}
  lines_settings = {'angle_count': 920,
                    'r_dim': 640,
                    'threshold': 0.7,
                    'min_angle': 15,
                    'min_rho': 15}

  segment_settings = {'angle_count': 920,
                      'r_dim': 640,
                      'threshold': 0.7,
                      'min_angle': 15,
                      'min_rho': 15,
                      'diff_max': 2,
                      'line_width_err': 2,
                      'min_seg_len': 40}
  corner_settings = {'sigma': 1,
                     'filter_size': 15,
                     'threshold': 0.128}
  rhombus_settings = {'angle_par_err_max': 0.1,
                      'angle_perp_err_max': 0.1}

  method2settings_dict = {Method.CANNY: canny_settings,
                          Method.NOTHING: nothing_settings,
                          Method.LINES: lines_settings,
                          Method.SEGMENTS: segment_settings,
                          Method.CORNERS: corner_settings,
                          Method.RHOMBUSES: rhombus_settings}

  strategy_enum2fn = {Strategy.SHI_TOMASI: shi_tomasi_r_score,
                      Strategy.HARRIS: harris_r_score,
                      Strategy.SAMPLE_ALL: sample_strategy_all,
                      Strategy.SAMPLE_EVERY_NTH: sample_strategy_every_nth,
                      Strategy.SAMPLE_PERCENTAGE: sample_strategy_percentage_rand,
                      Strategy.ADAPTED_PEAKS: adapted_hough_line_peaks,
                      Strategy.MY_PEAKS: my_hough_peaks,
                      Strategy.EXACT_LINES: retrieve_exact_lines,
                      Strategy.LONGER_LINES: retrieve_longer_lines}

  def get_canny_settings(self):
    return deepcopy(self.canny_settings)

  def get_nothing_settings(self):
    return deepcopy(self.nothing_settings)

  def get_lines_settings(self):
    return deepcopy(self.lines_settings)

  def get_segment_settings(self):
    return deepcopy(self.segment_settings)

  def get_corner_settings(self):
    return deepcopy(self.corner_settings)

  def get_rhombus_settings(self):
    return deepcopy(self.rhombus_settings)

  def get_method2settings_dict(self):
    return deepcopy(self.method2settings_dict)

  def get_strategy_enum2fn(self):
    return deepcopy(self.strategy_enum2fn)

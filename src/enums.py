from enum import Enum


class Target(Enum):
  DYNAMIC = 1
  STATIC = 2


class Method(Enum):
  LINES = 1
  SEGMENTS = 2
  CANNY = 3
  CORNERS = 4
  RHOMBUSES = 5
  NOTHING = 6


class Strategy(Enum):
  HARRIS = 1
  SHI_TOMASI = 2
  SAMPLE_ALL = 3
  SAMPLE_EVERY_NTH = 4
  SAMPLE_PERCENTAGE = 5
  ADAPTED_PEAKS = 6
  MY_PEAKS = 7
  EXACT_LINES = 8
  LONGER_LINES = 9

# Harris
# Shi_tomasi
# def sample_strategy_all(xs, ys):
# def sample_strategy_every_nth(xs, ys, n):
# def sample_strategy_percentage_rand(xs, ys, percentage):
# def adapted_hough_line_peaks(hough_arr, angles, rhos, min_rho, min_angle, threshold, show):
# def my_hough_peaks(hough_arr, angles, rhos, min_rho, min_angle, threshold, show):
# def retrieve_exact_lines(rhos, angles, N, M):
# def retrieve_longer_lines(rhos, angles, N, M):

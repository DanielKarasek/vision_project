import numpy as np


def shi_tomasi_r_score(Ixx, Iyy, Ixy):
  a = 1
  b = -(Ixx + Iyy)
  c = -(Ixy ** 2) + Ixx * Iyy
  lam_1 = (-b + np.sqrt(b ** 2 - 4 * a * c + 1e-12)) / (2 * a)
  lam_2 = (-b - np.sqrt(b ** 2 - 4 * a * c + 1e-12)) / (2 * a)
  return np.where(lam_1 < lam_2, lam_1, lam_2)


def harris_r_score(Ixx, Iyy, Ixy, k):
  det = Ixx * Iyy - Ixy * Ixy  # prod eigenvalues
  trace = Ixx + Iyy  # sum of eigen values
  r_score = det - k * (trace * trace)
  return r_score

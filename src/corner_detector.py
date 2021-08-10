import cv2
import numpy as np
from scipy.ndimage import convolve as fast_convolve
from scipy.ndimage.filters import gaussian_filter

from auxiliary import find_2dmax
from r_score_strategies import shi_tomasi_r_score


class CornerDetector:
  def __init__(self,
               r_score_fn=shi_tomasi_r_score):
    self.r_score_fn = r_score_fn

  def __call__(self, img, threshold=0.5, sigma=1.0, filter_size=20, show=False):
    if len(img.shape) == 3:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img.max() > 1:
      img = np.asarray(img, dtype=np.float32) / 255

    img = gaussian_filter(img, sigma=sigma)
    Ixx, Iyy, Ixy = self.find_derivs(img)
    r_score = self.r_score_fn(Ixx, Iyy, Ixy)
    centers = find_2dmax(r_score, filter_size, threshold, mode="reflect", show=show)
    centers = np.asarray(centers.T, dtype=int)

    if show:
      for (x, y) in zip(centers[:, 0], centers[:, 1]):
        cv2.circle(img, (x, y), 5, 1)
      cv2.imshow("corners", img)
    return centers

  def change_r_score_strategy(self, new_r_score_fn):
    self.r_score_fn = new_r_score_fn

  @staticmethod
  def find_derivs(img):
    Kx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    sum_filter = np.ones((3, 3))

    Ix = fast_convolve(img, Kx, mode="nearest")
    Iy = fast_convolve(img, Ky, mode="nearest")

    Ixx = Ix ** 2
    Iyy = Iy ** 2
    Ixy = Ix * Iy

    Ixx = fast_convolve(Ixx, sum_filter)
    Iyy = fast_convolve(Iyy, sum_filter)
    Ixy = fast_convolve(Ixy, sum_filter)

    return Ixx, Iyy, Ixy



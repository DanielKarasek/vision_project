import cv2
import numpy as np
from scipy.ndimage import convolve as fast_convolve
from scipy.ndimage.filters import gaussian_filter


def thresholdless_canny(img, auto_threshold=0.33, sigma=1, show=False):
  if len(img.shape) == 3:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  if img.max() > 1:
    img = np.asarray(img, dtype=np.float32) / 255

  med = np.median(img)

  high_threshold = 0.2#np.max([0, med*(1.0-auto_threshold)])
  low_threshold = 0.1#np.min([1, med * (1.0+auto_threshold)])

  return canny(img,
               double_threshold_low=low_threshold,
               double_threshold_high=high_threshold,
               sigma=sigma,
               show=show)


def canny(img, double_threshold_low=0.1, double_threshold_high=0.2, sigma=1, show=False):
  if len(img.shape) == 3:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  if img.max() > 1:
    img = np.asarray(img, dtype=np.float32) / 255

  filtered = gaussian_filter(img, sigma=sigma)
  intensities, directions = find_derivs(filtered, show=show)
  non_max_suppressed = non_max_suppression(intensities, directions, show=show)

  thresholded = double_threshold(non_max_suppressed,
                                 low_threshold=double_threshold_low,
                                 high_threshold=double_threshold_high,
                                 show=show)

  return hysteresis(thresholded, show=show)


class CannyWrapper:
  def __init__(self, canny_strategy_fn=thresholdless_canny):
    self.canny_fn = canny_strategy_fn

  def __call__(self, img, sigma=1):
    return self.canny_fn(img, sigma=sigma)

  def change_strategy(self, new_canny_fn):
    self.canny_fn = new_canny_fn


def find_derivs(img, show=False):
  Kx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
  Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

  Ix = fast_convolve(img, Kx, mode="nearest")
  Iy = fast_convolve(img, Ky, mode="nearest")

  g = np.hypot(Ix, Iy)
  g = g / g.max()

  if show:
    cv2.imshow("grads", g)
  return g, np.arctan2(Ix, Iy)


def non_max_suppression(intensities, directions, show=False):
  res = np.copy(intensities)

  N, M = intensities.shape

  padded = np.zeros((N + 1, M + 1))
  padded[:N, :M] = intensities
  qs = np.zeros((N, M))
  rs = np.zeros((N, M))

  directions = np.floor(16 * ((directions + np.pi) / (2 * np.pi)))

  coords = np.where((directions == 0) | (directions == 7) |
                    (directions == 8) | (directions == 15) | (directions == 16))
  qs[coords[0], coords[1]] = padded[coords[0] + 1, coords[1]]
  rs[coords[0], coords[1]] = padded[coords[0] - 1, coords[1]]

  coords = np.where((directions == 1) | (directions == 2) |
                    (directions == 9) | (directions == 10))
  qs[coords[0], coords[1]] = padded[coords[0] + 1, coords[1] + 1]
  rs[coords[0], coords[1]] = padded[coords[0] - 1, coords[1] - 1]

  coords = np.where((directions == 3) | (directions == 4) |
                    (directions == 11) | (directions == 12))
  qs[coords[0], coords[1]] = padded[coords[0], coords[1] + 1]
  rs[coords[0], coords[1]] = padded[coords[0], coords[1] - 1]

  coords = np.where((directions == 5) | (directions == 6) |
                    (directions == 13) | (directions == 14))
  qs[coords[0], coords[1]] = padded[coords[0] + 1, coords[1] - 1]
  rs[coords[0], coords[1]] = padded[coords[0] - 1, coords[1] + 1]

  res = res * np.asarray(qs < res, dtype=np.int32)
  res = res * np.asarray(rs < res, dtype=np.int32)

  if show:
    cv2.imshow("nonMaxSurpr", res)
  return res


def double_threshold(img, low_threshold=0.1, high_threshold=0.2, show=False):
  low_threshold = img.max() * low_threshold
  high_threshold = img.max() * high_threshold

  res = np.zeros_like(img)
  weak_indices = np.where((img >= low_threshold) & (img < high_threshold))
  strong_indices = np.where(img >= high_threshold)

  res[weak_indices[0], weak_indices[1]] = 0.2
  res[strong_indices[0], strong_indices[1]] = 1
  if show:
    cv2.imshow("doubleThreshhold", res)
  return res


def hysteresis(img, weak=0.2, strong=1, show=False):
  weak_arr = np.where(img == weak, True, False)
  strong_arr = np.where(img == strong, True, False)
  # very approximate way to do hysteresis without queues and stuff
  # try queue = np.where -> queue -> some vectorization for each (for one, nb vectorize?)
  for _ in np.arange(50):
    strong_arr[:-1, :] = (strong_arr[1:, :] & weak_arr[:-1, :]) | strong_arr[:-1, :]
    strong_arr[1:, :] = (strong_arr[:-1, :] & weak_arr[1:, :]) | strong_arr[1:, :]
    strong_arr[:, :-1] = (strong_arr[:, 1:] & weak_arr[:, :-1]) | strong_arr[:, :-1]
    strong_arr[:, 1:] = (strong_arr[:, :-1] & weak_arr[:, 1:]) | strong_arr[:, 1:]
    strong_arr[:-1, :-1] = (strong_arr[1:, 1:] & weak_arr[:-1, :-1]) | strong_arr[:-1, :-1]
    strong_arr[1:, 1:] = (strong_arr[:-1, :-1] & weak_arr[1:, 1:]) | strong_arr[1:, 1:]
    strong_arr[1:, :-1] = (strong_arr[:-1, 1:] & weak_arr[1:, :-1]) | strong_arr[1:, :-1]
    strong_arr[:-1, 1:] = (strong_arr[1:, :-1] & weak_arr[:-1, 1:]) | strong_arr[:-1, 1:]

  strong_arr = np.asarray(strong_arr, dtype=np.float32)

  if show:
    cv2.imshow("Hysteresis", strong_arr)
  return strong_arr

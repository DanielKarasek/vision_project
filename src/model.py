import os

from enums import *

from canny import CannyWrapper
from corner_detector import *
from hough_lines import HoughFullLines, HoughSegments
from rhombuses import find_rhombuses

from data2picklelatte import Database


# mozna by se pak dalo pridat settings
# tech strategii, a delat to podobne
# jen misto volani by pak bylo "update strategies" pomoci dict
# noinspection PyArgumentList
class Model:

  def __init__(self):
    self.method_dict = {Method.CANNY: self.canny_fn,
                        Method.NOTHING: self.return_same,
                        Method.LINES: self.lines,
                        Method.SEGMENTS: self.segments,
                        Method.CORNERS: self.corners,
                        Method.RHOMBUSES: self.rhombuses}

    self.target = Target.STATIC

    self.method = Method.CANNY

    self.hough_lines = HoughFullLines()
    self.hough_segments = HoughSegments()
    self.corner_detector = CornerDetector()
    self.canny_wrapper = CannyWrapper()

    #pickle this shit
    db = Database()

    self.settings = db.get_method2settings_dict()
    self.strategy2fn = db.get_strategy_enum2fn()

    self.static_image = cv2.imread("../test_images/chessboard2.jpg")
    self.update_static()

    self.camera = cv2.VideoCapture(-1)

  def change_sample_strategy(self, method, new_strategy):
    if method == Method.LINES:
      self.hough_lines.change_sample_strategy(new_strategy)
    else:
      self.hough_segments.change_sample_strategy(new_strategy)
    self.update_static()

  def change_hough_peaks_strategy(self, method, new_strategy):
    if method == Method.LINES:
      self.hough_lines.change_hough_peaks_strategy(new_strategy)
    else:
      self.hough_segments.change_hough_peaks_strategy(new_strategy)
    self.update_static()

  def change_retrieve_lines_strategy(self, new_strategy):
    self.hough_lines.change_retrieve_lines_strategy(new_strategy)
    self.update_static()

  def change_r_score_strategy(self, new_strategy):
    self.corner_detector.change_r_score_strategy(new_strategy)
    self.update_static()

  def copy_settings_lines2segments(self):
    for key, value in self.settings[Method.LINES].items():
      if key in self.settings[Method.SEGMENTS].keys():
        self.settings[Method.SEGMENTS][key] = value

  def change_setting(self, method, keyword, value):
    self.settings[method][keyword] = value
    self.update_static()

  def change_settings(self, method, new_settings_dictionary):
    for key, value in new_settings_dictionary.items():
      self.settings[method][key] = value
    self.update_static()

  def get_settings(self, method):
    return self.settings[method]

  def change_method(self, method):
    self.method = method
    self.update_static()

  def return_same(self, img):
    img = gaussian_filter(img, **self.settings[Method.NOTHING])
    return img

  def canny_fn(self, img):
    return self.canny_wrapper(img, **self.settings[Method.CANNY])

  def lines(self, img):
    cannied = self.canny_wrapper(img, **self.settings[Method.CANNY])
    lines, _ = self.hough_lines(cannied, **self.settings[Method.LINES])
    for line in lines:
      cv2.line(img, line[0], line[1], (255, 0, 0), 2)
    return img

  def segments(self, img):
    cannied = self.canny_wrapper(img, **self.settings[Method.CANNY])
    segments = self.hough_segments(cannied, **self.settings[Method.SEGMENTS])
    for segment in segments:
      cv2.line(img, segment[0], segment[1], (0, 255, 0), 2)
    return img

  def corners(self, img):
    corners = self.corner_detector(img, **self.settings[Method.CORNERS])
    for corner in corners.T:
      cv2.circle(img, corner, 3, (255, 0, 0), -1)
    return img

  def rhombuses(self, img):
    cannied = self.canny_wrapper(img, **self.settings[Method.CANNY])
    _, lines_r_angle = self.hough_lines(cannied, **self.settings[Method.LINES])

    N, M = cannied.shape

    rhombuses = find_rhombuses(lines_r_angle, N, M, **self.settings[Method.RHOMBUSES])

    color = 0
    for rhomb in rhombuses:
      rhomb = rhomb.reshape((-1, 1, 2))
      cv2.polylines(img, [rhomb], True, (0, color, 0), 3)
      color = (color+10) % 255

    return img

  def update_static(self):
    method_fn = self.method_dict[self.method]
    self.processed_static_image = method_fn(np.copy(self.static_image))

  def change_static_image(self, name):
    self.static_image = cv2.imread("../test_images/" + name)
    self.static_image = cv2.cvtColor(self.static_image, cv2.COLOR_BGR2RGB)
    self.update_static()

  def get_available_images(self):
    return os.listdir("../test_images")

  def get_dynamic_proccesed(self):
    ret, frame = self.camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    method_fn = self.method_dict[self.method]
    return method_fn(frame)

  def get_frame(self):
    if self.target == Target.STATIC:
      return self.processed_static_image
    else:
      return self.get_dynamic_proccesed()

  def set_target(self, target: Target):
    self.target = target

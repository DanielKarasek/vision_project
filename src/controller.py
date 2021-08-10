import numpy as np

from enums import *


class Controller:
  def __init__(self, model, view):
    self.color = 0
    self.model = model
    self.view = view
    self.view.setup(self)

  def get_frame(self):
    img: np.ndarray
    img = self.model.get_frame()
    if img.dtype == np.float32 and img.max() <= 1:
      img = np.asarray(img * 255, np.uint8)
    return img

  def static_image_menu(self):
    available_images = self.model.get_available_images()
    self.view.create_select_image_popoup(available_images)

  def new_static_image_chosen(self, chosen):
    self.model.change_static_image(chosen)
    self.view.destroy_popup_menu()

  def change_method_pressed(self, method):
    if type(Method.CANNY) != type(method):
      return
    self.model.change_method(method)
    settings = self.model.get_settings(method)
    self.view.swap_method_specific_views(method, settings)

  def change_target_pressed(self, target):
    if type(Target.STATIC) != type(target):
      return
    self.model.set_target(target)

  def change_setting_pressed(self, method, keyword, value):
    self.model.change_setting(method, keyword, value)

  def change_apply_settings(self, method, new_settings_dictionary):
    self.model.change_settings(method, new_settings_dictionary)

  def copy_lines_settings_pressed(self):
    self.model.copy_settings_lines2segments()

  def back2method_settings_pressed(self):
    self.view.show_method_settings()

  def go2strategy_settings_pressed(self):
    self.view.show_strategy_settings()

  def run(self):
    self.view.mainloop()

  def change_sample_strategy(self, method, new_strategy):
    self.model.change_sample_strategy(method, new_strategy)

  def change_hough_peaks_strategy(self, method, new_strategy):
    self.model.change_hough_peaks_strategy(method, new_strategy)

  def change_retrieve_lines_strategy(self, new_strategy):
    self.model.change_retrieve_lines_strategy(new_strategy)

  def change_r_score_strategy(self, new_strategy):
    self.model.change_r_score_strategy(new_strategy)
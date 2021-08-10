import tkinter as tk

import numpy as np

from enums import Method


class MethodSettingFrame(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)

    self.canny_setting_view = CannyMethodSettings(self, controller)
    self.line_setting_view = LineMethodSettings(self, controller)
    self.corner_setting_view = CornerMethodSettings(self, controller)
    self.segments_setting_view = SegmentsMethodSettings(self, controller)
    self.rhombuses_setting_view = RhombusMethodSettings(self, controller)
    self.nothing_setting_view = NothingMethodSettings(self, controller)

    self.views_dict = {Method.LINES: self.line_setting_view,
                       Method.CANNY: self.canny_setting_view,
                       Method.CORNERS: self.corner_setting_view,
                       Method.SEGMENTS: self.segments_setting_view,
                       Method.RHOMBUSES: self.rhombuses_setting_view,
                       Method.NOTHING: self.nothing_setting_view}

    self.canny_setting_view.grid(row=0, column=0, sticky="nsew")
    self.current_setting = self.canny_setting_view

  def change_setting_view(self, method, settings):
    self.current_setting.grid_forget()
    new_setting = self.views_dict[method]
    new_setting.set_values(settings)
    new_setting.grid(row=0, column=0, sticky="nsew")
    self.current_setting = new_setting


class BaseMethodSettings(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    self.controller = controller
    self.dict = {}
    self.apply_button = None

    self.method = Method.NOTHING

  def set_values(self, settings):
    for key, value in self.dict.items():
      key.set(settings[value])

  def apply(self):
    settings_dict = {}
    for key, value in self.dict.items():
      settings_dict[value] = key.get()
    self.controller.change_apply_settings(self.method, settings_dict)

  def append_apply_button(self, total_widgets):
    self.apply_button = tk.Button(self, text="apply", command=self.apply)
    self.apply_button.grid(row=total_widgets+1, column=0, sticky="nsew")

  def add_widgets_to_grid(self):
    for key, num in zip(self.dict.keys(), np.arange(len(self.dict))+1):
      key.grid(row=num, column=0, sticky="nsew")

  def setup(self, method, title_text):
    title = tk.Label(self, text=title_text)
    title.grid(row=0, column=0, sticky="n")

    self.method = method
    self.add_widgets_to_grid()
    self.append_apply_button(len(self.dict))


class CannyMethodSettings(BaseMethodSettings):

  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    self.sigma = tk.Scale(self,
                          from_=0,
                          to=5,
                          label="sigma",
                          orient=tk.HORIZONTAL,
                          resolution=0.01,
                          digits=0)

    self.dict = {self.sigma: 'sigma'}
    self.setup(Method.CANNY, "Canny method settings")


class LineMethodSettings(BaseMethodSettings):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    self.threshold = tk.Scale(self,
                              from_=0,
                              to=1,
                              label="threshold",
                              orient=tk.HORIZONTAL,
                              resolution=0.005)

    self.angle = tk.Scale(self,
                          from_=300,
                          to=2000,
                          label="angle count",
                          orient=tk.HORIZONTAL,
                          resolution=1)

    self.rho_dim = tk.Scale(self,
                            from_=300,
                            to=2000,
                            label="rho dimension",
                            orient=tk.HORIZONTAL,
                            resolution=1)

    self.min_rho = tk.Scale(self,
                            from_=5,
                            to=500,
                            label="minimal rho difference",
                            orient=tk.HORIZONTAL,
                            resolution=1)
    self.min_angle = tk.Scale(self,
                              from_=1,
                              to=50,
                              label="minimal angle difference",
                              orient=tk.HORIZONTAL,
                              resolution=1)

    self.dict = {self.threshold: 'threshold',
                 self.angle: 'angle_count',
                 self.rho_dim: 'r_dim',
                 self.min_angle: 'min_angle',
                 self.min_rho: 'min_rho'}

    self.setup(Method.LINES, "Canny method settings")
    self.copy_button = tk.Button(self, text="copy settings to segments", command=controller.copy_lines_settings_pressed)
    self.strategy_button = tk.Button(self, text="change strategies",
                                     command=controller.go2strategy_settings_pressed)
    self.copy_button.grid(row=len(self.dict)+2, column=0, sticky="nsew")
    self.strategy_button.grid(row=len(self.dict)+3, column=0, sticky="nsew")


class CornerMethodSettings(BaseMethodSettings):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    self.sigma = tk.Scale(self,
                          from_=0,
                          to=5,
                          label="sigma",
                          orient=tk.HORIZONTAL,
                          resolution=0.01,
                          digits=0)

    self.filter_size = tk.Scale(self,
                                from_=5,
                                to=50,
                                label="max suppression size",
                                orient=tk.HORIZONTAL,
                                resolution=1,
                                digits=0)

    self.threshold = tk.Scale(self,
                              from_=0,
                              to=1,
                              label="threshold",
                              orient=tk.HORIZONTAL,
                              resolution=0.001,
                              digits=0)

    self.dict = {self.sigma: 'sigma',
                 self.filter_size: 'filter_size',
                 self.threshold: 'threshold'}

    self.setup(Method.CORNERS, "Corner method settings")
    self.strategy_button = tk.Button(self, text="change strategies",
                                     command=controller.go2strategy_settings_pressed)
    self.strategy_button.grid(row=len(self.dict)+2, column=0, sticky="nsew")


class SegmentsMethodSettings(BaseMethodSettings):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)
    self.threshold = tk.Scale(self,
                              from_=0,
                              to=1,
                              label="threshold",
                              orient=tk.HORIZONTAL,
                              resolution=0.005)

    self.angle = tk.Scale(self,
                          from_=300,
                          to=2000,
                          label="angle count",
                          orient=tk.HORIZONTAL,
                          resolution=1)

    self.rho_dim = tk.Scale(self,
                            from_=300,
                            to=2000,
                            label="rho dimension",
                            orient=tk.HORIZONTAL,
                            resolution=1)

    self.min_rho = tk.Scale(self,
                            from_=5,
                            to=500,
                            label="minimal rho difference",
                            orient=tk.HORIZONTAL,
                            resolution=1)
    self.min_angle = tk.Scale(self,
                              from_=1,
                              to=50,
                              label="minimal angle difference",
                              orient=tk.HORIZONTAL,
                              resolution=1)

    self.diff_max = tk.Scale(self,
                             from_=0,
                             to=20,
                             label="max space between segments points",
                             orient=tk.HORIZONTAL,
                             resolution=0.1)
    self.line_width_err = tk.Scale(self,
                                   from_=1,
                                   to=10,
                                   label="rho off line tolerance",
                                   orient=tk.HORIZONTAL,
                                   resolution=1)
    self.min_seg_len = tk.Scale(self,
                                from_=5,
                                to=1000,
                                label="minimal segment lenght",
                                orient=tk.HORIZONTAL,
                                resolution=1)

    self.dict = {self.threshold: 'threshold',
                 self.angle: 'angle_count',
                 self.rho_dim: 'r_dim',
                 self.min_angle: 'min_angle',
                 self.min_rho: 'min_rho',
                 self.diff_max: 'diff_max',
                 self.line_width_err: 'line_width_err',
                 self.min_seg_len: 'min_seg_len'}
    self.setup(Method.SEGMENTS, "Segments method settings")

    self.strategy_button = tk.Button(self, text="change strategies",
                                     command=controller.go2strategy_settings_pressed)
    self.strategy_button.grid(row=len(self.dict)+2, column=0, sticky="nsew")


class RhombusMethodSettings(BaseMethodSettings):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    self.angle_max_parallel_error = tk.Scale(self,
                                             from_=0,
                                             to=90,
                                             label="max parallel lines angle diff",
                                             orient=tk.HORIZONTAL,
                                             resolution=0.1,
                                             digits=0)

    self.angle_max_perpendicular_error = tk.Scale(self,
                                                  from_=0,
                                                  to=90,
                                                  label="max perpendicular lines angle diff",
                                                  orient=tk.HORIZONTAL,
                                                  resolution=0.1,
                                                  digits=0)

    self.dict = {self.angle_max_parallel_error: 'angle_par_err_max',
                 self.angle_max_perpendicular_error: 'angle_perp_err_max'}

    self.setup(Method.RHOMBUSES, 'Rhombuses method settings')

  def apply(self):
    settings_dict = {}
    for key, value in self.dict.items():
      settings_dict[value] = key.get()*180/np.pi
    self.controller.change_apply_settings(self.method, settings_dict)


class NothingMethodSettings(BaseMethodSettings):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="Nothing setting frame")
    title.grid(row=0, column=0, sticky="n")

    self.sigma = tk.Scale(self,
                          from_=0,
                          to=5,
                          label="sigma",
                          orient=tk.HORIZONTAL,
                          resolution=0.01,
                          digits=0)

    self.dict = {self.sigma: 'sigma'}

    self.setup(Method.NOTHING, "Nothing method setting")
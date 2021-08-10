import tkinter as tk
import tkinter.ttk as ttk

from r_score_strategies import *
from line_find_strategies import *
from peak_find_strategies import *
from sample_strategies import *


def donothing():
  pass


class BaseChoosePopup(tk.Toplevel):
  def __init__(self, controller):
    super().__init__()
    self.wm_title("select strategy")

    self.grid_columnconfigure(0, weight=1, uniform="column")
    self.grid_columnconfigure(2, weight=1, uniform="column")
    self.grid_columnconfigure(4, weight=1, uniform="column")

    self.grid_rowconfigure(0, weight=1)
    ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=1, sticky="nsew")
    ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=3, sticky="nsew")
    self.controller = controller


class HoughPeaksPopup(BaseChoosePopup):
  def __init__(self, method, controller):
    super().__init__(controller)
    scipy_peaks_setting = ScipyHoughPeaksSettings(self, method, controller)
    my_peaks_settings = MyHoughPeaksSettings(self, method, controller)

    scipy_peaks_setting.grid(row=0, column=0, sticky="nsew")
    my_peaks_settings.grid(row=0, column=2, sticky="nsew")


class SamplePopup(BaseChoosePopup):
  def __init__(self, method, controller):
    super().__init__(controller)
    sample_all_settings = SampleAllSettings(self, method, controller)
    sample_every_nth_settings = SampleEveryNthSetting(self, method, controller)
    sample_random_settings = SampleRandomSettings(self, method, controller)

    sample_all_settings.grid(row=0, column=0, sticky="nsew")
    sample_every_nth_settings.grid(row=0, column=2, sticky="nsew")
    sample_random_settings.grid(row=0, column=4, sticky="nsew")


class LineRetrievePopup(BaseChoosePopup):
  def __init__(self, controller):
    super().__init__(controller)
    longer_lines_settings = RetriveLongerLinesSettings(self, controller)
    exact_lines_settings = RetrieveExactLinesSettings(self, controller)

    longer_lines_settings.grid(row=0, column=0, sticky="nsew")
    exact_lines_settings.grid(row=0, column=2, sticky="nsew")


class RScorePopup(BaseChoosePopup):
  def __init__(self, controller):
    super().__init__(controller)
    harris = HarrisSettings(self, controller)
    shi_tomasi = ShiTomasiSetting(self, controller)

    harris.grid(row=0, column=0, sticky="nsew")
    shi_tomasi.grid(row=0, column=2, sticky="nsew")


class HarrisSettings(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="harris strategy")

    self.k_scale = tk.Scale(self,
                            from_=0.02,
                            to=0.15,
                            resolution=0.01,
                            orient=tk.HORIZONTAL,
                            label="k value")
    strategy_fn = lambda Ixx, Iyy, Ixy: harris_r_score(Ixx, Iyy, Ixy, self.k_scale.get())
    command_fn = lambda: controller.change_r_score_strategy(strategy_fn)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.k_scale.grid(row=1, column=0)
    self.apply_button.grid(row=2, column=0)


class ShiTomasiSetting(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="shi-tomasi strategy")

    command_fn = lambda: controller.change_r_score_strategy(shi_tomasi_r_score)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.grid(row=1, column=0)
    self.apply_button.grid(row=2, column=0)


class ScipyHoughPeaksSettings(tk.Frame):
  def __init__(self, parent, method, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="scipy hough peaks strategy")

    command_fn = lambda: controller.change_hough_peaks_strategy(method, adapted_hough_line_peaks)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.grid(row=1, column=0)
    self.apply_button.grid(row=2, column=0)


class MyHoughPeaksSettings(tk.Frame):
  def __init__(self, parent, method, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="my hough peaks strategy")

    command_fn = lambda: controller.change_hough_peaks_strategy(method, my_hough_peaks)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.grid(row=1, column=0)
    self.apply_button.grid(row=2, column=0)


class SampleAllSettings(tk.Frame):
  def __init__(self, parent, method, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="Sample all strategy")

    command_fn = lambda: controller.change_sample_strategy(method, sample_strategy_all)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.apply_button.grid(row=2, column=0)


class SampleEveryNthSetting(tk.Frame):
  def __init__(self, parent, method, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="Sample every Nth point")

    self.nth = tk.Scale(self,
                        from_=1,
                        to=20,
                        resolution=1,
                        orient=tk.HORIZONTAL,
                        label="N")

    new_fn = lambda xs, ys: sample_strategy_every_nth(xs, ys, self.nth.get())
    command_fn = lambda: controller.change_sample_strategy(method, new_fn)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.nth.grid(row=1, column=0)
    self.apply_button.grid(row=2, column=0)


class SampleRandomSettings(tk.Frame):
  def __init__(self, parent, method, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="Sample random percentage")

    self.percentage = tk.Scale(self,
                               from_=1,
                               to=100,
                               resolution=1,
                               orient=tk.HORIZONTAL,
                               label="percentage")
    new_fn = lambda xs, ys: sample_strategy_percentage_rand(xs, ys, float(self.percentage.get())/100)
    command_fn = lambda: controller.change_sample_strategy(method, new_fn)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.percentage.grid(row=1, column=0)
    self.apply_button.grid(row=2, column=0)


class RetriveLongerLinesSettings(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="Retrieve longer lines strategy")

    command_fn = lambda: controller.change_retrieve_lines_strategy(retrieve_longer_lines)
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.apply_button.grid(row=2, column=0)


class RetrieveExactLinesSettings(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.grid_columnconfigure(0, weight=1)

    title = tk.Label(self, text="Retrieve exact lines strategy")

    command_fn = lambda: controller.change_retrieve_lines_strategy(retrieve_exact_lines())
    self.apply_button = tk.Button(self, text="apply", command=command_fn)
    title.grid(row=0, column=0)
    self.apply_button.grid(row=2, column=0)


# sample_strategy_all -> None
# shi_tomasi -> None
# sample_strategy_every_nth -> N
# sample_strategy_percentage_rand -> percentage
# harris -> k (0.02-0.15)

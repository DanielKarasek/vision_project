from popup_strategies_view import *
import tkinter as tk

from enums import *


def donothing():
  pass


class StrategyView(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)

    self.controller = controller

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.canny_strategy_view = CannyStrategyView(self, controller)
    self.line_strategy_view = LineStrategyView(self, controller)
    self.segment_strategy_view = SegmentStrategyView(self, controller)
    self.corner_strategy_view = CornerStrategyView(self, controller)

    self.views_dict = {Method.CANNY: self.canny_strategy_view,
                       Method.LINES: self.line_strategy_view,
                       Method.SEGMENTS: self.segment_strategy_view,
                       Method.CORNERS: self.corner_strategy_view,
                       Method.RHOMBUSES: self.canny_strategy_view,
                       Method.NOTHING: self.canny_strategy_view
                       }

    self.line_strategy_view.grid(row=0, column=0, sticky="nsew")
    self.current_setting = self.line_strategy_view

  def change_strategy_view(self, method):
    self.current_setting.grid_forget()
    new_setting = self.views_dict[method]
    new_setting.grid(row=0, column=0, sticky="nsew")
    self.current_setting = new_setting


class BaseStrategyView(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.grid_columnconfigure(0, weight=0)

    self.controller = controller

  def setup(self, topic_text, widgets):
    self.grid_columnconfigure(0, weight=1)

    label = tk.Label(self, text=topic_text, font=("times new roman", 10))
    label.grid(row=0, column=0, sticky="nsew")
    info_label = tk.Label(self, text="Choose which part of \nmethod to change", font=("times new roman", 9))
    info_label.grid(row=1, column=0, sticky="nsew")
    for widget, idx in zip(widgets, range(len(widgets))):
      widget.grid(row=idx+2, column=0, sticky="nsew")
    back_widget = tk.Button(self, text="back", command=self.controller.back2method_settings_pressed)
    back_widget.grid(row=len(widgets)+3, column=0)


class LineStrategyView(BaseStrategyView):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    sample_strategy = tk.Button(self, text="sample strategy",
                                command=lambda: SamplePopup(Method.LINES, controller))
    hough_peaks_strategy = tk.Button(self, text="hough peaks strategy",
                                     command=lambda: HoughPeaksPopup(Method.LINES, controller))
    line_retrieve_strategy = tk.Button(self, text="line retrieve strategy",
                                       command=lambda: LineRetrievePopup(controller))

    self.setup("Line strategy view", [sample_strategy, hough_peaks_strategy, line_retrieve_strategy])


class CannyStrategyView(BaseStrategyView):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    canny_strategy = tk.Button(self, text="canny strategy", command=donothing)
    self.setup("Canny strategy view", [canny_strategy])


class SegmentStrategyView(BaseStrategyView):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    sample_strategy = tk.Button(self, text="sample strategy",
                                command=lambda: SamplePopup(Method.SEGMENTS, controller))
    hough_peaks_strategy = tk.Button(self, text="hough peaks strategy",
                                     command=lambda: HoughPeaksPopup(Method.SEGMENTS, controller))

    self.setup("Segment strategy view", [sample_strategy, hough_peaks_strategy])


class CornerStrategyView(BaseStrategyView):
  def __init__(self, parent, controller):
    super().__init__(parent, controller)

    r_score_strategy = tk.Button(self, text="r score strategy", command=lambda: RScorePopup(self.controller))

    self.setup("Corner strategy view", [r_score_strategy])

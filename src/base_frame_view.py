import tkinter as tk

from result_frame_view import ResultFrame
from method_settings import MethodSettingFrame
from choose_strategy_view import StrategyView


class BaseFrame(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.result_frame = ResultFrame(self, controller)
    self.method_settings = MethodSettingFrame(self, controller)
    self.strategy_choice = StrategyView(self, controller)

    self.grid_columnconfigure(0, weight=2, uniform="column")
    self.grid_columnconfigure(1, weight=1, uniform="column")
    self.grid_rowconfigure(0, weight=1)

    self.result_frame.grid(row=0, column=0, sticky="nsew")
    self.method_settings.grid(row=0, column=1, sticky="nsew")

    self.current_choice_frame = self.method_settings

    self.result_frame.after(1, lambda: self.result_frame.update_image())

  def swap_method_specific_views(self, method, settings):
    self.method_settings.change_setting_view(method, settings)
    self.strategy_choice.change_strategy_view(method)

  def show_method_settings(self):
    self.current_choice_frame.grid_forget()
    self.method_settings.grid(row=0, column=1, sticky="nsew")
    self.current_choice_frame = self.method_settings

  def show_strategy_settings(self):
    self.current_choice_frame.grid_forget()
    self.strategy_choice.grid(row=0, column=1, sticky="nsew")
    self.current_choice_frame = self.strategy_choice
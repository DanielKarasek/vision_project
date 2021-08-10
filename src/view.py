import tkinter as tk

from enums import *
from popup_menu_view import PopUpMenu
from base_frame_view import BaseFrame


def do_nothing():
  pass


# noinspection PyAttributeOutsideInit
class View(tk.Tk):

  def setup(self, controller):
    self.title('Vision project')

    self.geometry('640x480')

    self.controller = controller
    self.menubar = self.create_menubar()
    self.base_frame = self.create_base_window()

    self.popup_menu = None

  def swap_method_specific_views(self, method, settings):
    self.base_frame.swap_method_specific_views(method, settings)

  def show_method_settings(self):
    self.base_frame.show_method_settings()

  def show_strategy_settings(self):
    self.base_frame.show_strategy_settings()

  def create_base_window(self):
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)

    base_frame = BaseFrame(self, self.controller)
    base_frame.grid(row=0, column=0, sticky="nsew")
    return base_frame

  def create_menubar(self):
    menubar = tk.Menu(self)
    target_menu = self.create_target_menu(menubar)
    operation_menu = self.create_operation_menu(menubar)
    menubar.add_cascade(label="target", menu=target_menu)
    menubar.add_cascade(label="operation", menu=operation_menu)
    self.config(menu=menubar)
    return menubar

  def create_target_menu(self, menubar):
    target_menu = tk.Menu(menubar, tearoff=0)
    target_menu.add_command(label="static", command=lambda: self.controller.change_target_pressed(Target.STATIC))
    target_menu.add_command(label="dynamic", command=lambda: self.controller.change_target_pressed(Target.DYNAMIC))
    target_menu.add_separator()
    target_menu.add_command(label="static image", command=self.controller.static_image_menu)
    return target_menu

  def create_operation_menu(self, menubar):
    operation_menu = tk.Menu(menubar, tearoff=0)
    operation_menu.add_command(label="lines", command=lambda: self.controller.change_method_pressed(Method.LINES))
    operation_menu.add_command(label="segment", command=lambda: self.controller.change_method_pressed(Method.SEGMENTS))
    operation_menu.add_command(label="corners", command=lambda: self.controller.change_method_pressed(Method.CORNERS))
    operation_menu.add_command(label="rhombuses", command=lambda: self.controller.change_method_pressed(Method.RHOMBUSES))
    operation_menu.add_command(label="canny", command=lambda: self.controller.change_method_pressed(Method.CANNY))
    operation_menu.add_command(label="nothing", command=lambda: self.controller.change_method_pressed(Method.NOTHING))
    return operation_menu

  def create_select_image_popoup(self, available_images):
    self.popup_menu = PopUpMenu(available_images, self.controller)

  def destroy_popup_menu(self):
    if self.popup_menu:
      self.popup_menu.destroy()
      self.popup_menu = None

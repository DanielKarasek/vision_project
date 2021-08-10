import tkinter as tk


class PopUpMenu(tk.Toplevel):
  def __init__(self, images_names, controller):
    super().__init__()
    self.wm_title("static image select")

    self.grid_rowconfigure(0, weight=5, uniform="row")
    self.grid_rowconfigure(1, weight=1, uniform="row")

    self.grid_columnconfigure(0, weight=1)

    self.controller = controller

    self.image_names_listbox = tk.Listbox(self)
    for image_name in images_names:
      self.image_names_listbox.insert(tk.END, image_name)
    self.image_names_listbox.grid(row=0, column=0, sticky="nsew")
    button = tk.Button(self, text="choose selected", command=self.image_chosen)
    button.grid(row=1, column=0, pady=15, sticky="n")
    self.geometry("250x300")

  def image_chosen(self):
    if self.image_names_listbox.curselection():
      chosen = self.image_names_listbox.get(self.image_names_listbox.curselection())
      self.controller.new_static_image_chosen(chosen)
    else:
      pass

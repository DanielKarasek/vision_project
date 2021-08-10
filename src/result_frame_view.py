import time
import tkinter as tk

from PIL import Image, ImageTk


class ResultFrame(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1, uniform="row")
    self.grid_rowconfigure(1, weight=30, uniform="row")
    self.grid_rowconfigure(2, weight=2, uniform="row")

    label = tk.Label(self, text="result frame", background="green")
    label.grid(row=0, column=0, sticky="n")
    self.canvas = tk.Canvas(self)
    self.canvas.grid(row=1, column=0, sticky="nsew")

    self.canvas.configure(background="blue")
    self.canvas.configure(highlightthickness=0)

    self.configure(background="green")

    snapshot_button = tk.Button(self, text="take snapshot", command=controller.take_snapshot)
    snapshot_button.grid(row=2, column=0)
    self.img = None

  def update_image(self):
    start = time.time()
    frame_arr = self.controller.get_frame()

    self.canvas.update()
    w = self.canvas.winfo_width()
    h = self.canvas.winfo_height()

    img = ImageTk.PhotoImage(Image.fromarray(frame_arr).resize((w, h)))
    self.img = img

    self.canvas.create_image(w, h, anchor=tk.SE, image=img)
    end = time.time()
    time2wait = int(10-(end-start))
    if time2wait <= 0:
      time2wait = 1
    self.after(time2wait, lambda: self.update_image())



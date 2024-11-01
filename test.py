# TODO: DELETE THIS WHEN YOU PUBLISH

import tkinter as tk

win=tk.Tk()
win.geometry("100x100")

default=tk.DoubleVar(value=10)

scale=tk.Scale(win,from_=1,to=20,variable=default)
scale.pack()

win.mainloop()
import tkinter as tk
from tkinter import BOTH

class BLabel(tk.Label):
	def __init__(self, parent, width, height, text, font, fg, bg):

		#self.label = tk.Label(self.frame, width=width, height=height, text=text, fg=fg, bg=bg, font=font)




		self.frame = tk.Frame(parent, width=width, height=height, bg=parent['bg'])
		self.frame.pack_propagate(0)

		super(BLabel, self).__init__(self.frame, width=width, height=height, text=text, fg=fg, bg=bg, font=font)
		self.pack(fill=BOTH, expand=1)

	def place(self, x, y):
		self.frame.place(x=x, y=y)
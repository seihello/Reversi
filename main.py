import tkinter as tk
from MassType import MassType
from tkinter import messagebox
import sys
from tkinter import BOTH
from Game import Game

if __name__ == "__main__":
	root = tk.Tk()
	root.geometry('800x640')
	root.resizable(width=False, height=False)
	game = Game(root)
	root.mainloop()




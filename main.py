from Game import Game

import tkinter as tk

if __name__ == "__main__":
	root = tk.Tk()
	root.geometry('800x640')
	root.resizable(width=False, height=False)
	root.title('Reversi')
	game = Game(root)
	root.mainloop()




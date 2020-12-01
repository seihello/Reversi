from MassType import MassType
import tkinter as tk
from Common import Common

class Board:

	def __init__(self, canvas):
		self.canvas = canvas
		self.mass_list = [[0 for i in range(8)] for j in range(8)]
		for i in range(8):
			for j in range(8):
				self.mass_list[i][j] = Mass(self.canvas, i, j)

		self.mass_list[3][3].type = MassType.WHITE
		self.mass_list[3][4].type = MassType.BLACK
		self.mass_list[4][3].type = MassType.BLACK
		self.mass_list[4][4].type = MassType.WHITE

		self.draw_pieces() # 先手が黒なので逆を指定しておく

	def update(self, x, y, mass_type):
		if self.can_put(x, y, mass_type):
			self.mass_list[x][y].type = mass_type
			self.reverse(x, y, mass_type)
			return True
		else:
			return False

	def reverse(self, x, y, mass_type):
		self.reverse_1dir(x, y,  1,  1, mass_type)
		self.reverse_1dir(x, y,  0,  1, mass_type)
		self.reverse_1dir(x, y, -1,  1, mass_type)
		self.reverse_1dir(x, y, -1,  0, mass_type)
		self.reverse_1dir(x, y, -1, -1, mass_type)
		self.reverse_1dir(x, y,  0, -1, mass_type)
		self.reverse_1dir(x, y,  1, -1, mass_type)
		self.reverse_1dir(x, y,  1,  0, mass_type)

	def reverse_1dir(self, x, y, dx, dy, mass_type):
		searching_x = x
		searching_y = y

		if self.mass_list[x][y].type != mass_type:
			return 0

		opp_mass_type = Mass.get_opp_type(mass_type)

		while True:
			searching_x += dx
			searching_y += dy
			if 0 <= searching_x < Common.MASS_NUM and 0 <= searching_y < Common.MASS_NUM:
				if self.mass_list[searching_x][searching_y].type == mass_type:
					break
				elif self.mass_list[searching_x][searching_y].type == MassType.EMPTY:
					return 0
			else:
				return 0

		while True:
			searching_x -= dx
			searching_y -= dy
			if searching_x == x and searching_y == y:
				break
			else:
				self.mass_list[searching_x][searching_y].type = mass_type

	def draw_pieces(self):
		for i in range(8):
			for j in range(8):
				self.mass_list[i][j].draw()

	def delete_pieces(self):
		for i in range(8):
			for j in range(8):
				self.mass_list[i][j].delete()

	def draw_puttable(self, mass_type):
		print('draw_puttable ' + str(mass_type))
		for i in range(8):
			for j in range(8):
				puttable = self.can_put(i, j, mass_type)
				self.mass_list[i][j].draw_puttable(puttable)

	def delete_puttable(self):
		for i in range(8):
			for j in range(8):
				self.mass_list[i][j].delete_puttable()

	def can_put(self, x, y, mass_type):
		if self.mass_list[x][y].type != MassType.EMPTY:
			return False
		elif self.get_reversible_num(x, y, mass_type) <= 0:
			return False
		else:
			return True

	def can_put_somewhere(self, mass_type):
		for i in range(8):
			for j in range(8):
				if self.can_put(i, j, mass_type):
					return True
		return False

	def get_reversible_num(self, x, y, mass_type):
		num = 0
		num += self.get_reversible_num_1dir(x, y,  1,  1, mass_type)
		num += self.get_reversible_num_1dir(x, y,  0,  1, mass_type)
		num += self.get_reversible_num_1dir(x, y, -1,  1, mass_type)
		num += self.get_reversible_num_1dir(x, y, -1,  0, mass_type)
		num += self.get_reversible_num_1dir(x, y, -1, -1, mass_type)
		num += self.get_reversible_num_1dir(x, y,  0, -1, mass_type)
		num += self.get_reversible_num_1dir(x, y,  1, -1, mass_type)
		num += self.get_reversible_num_1dir(x, y,  1,  0, mass_type)
		return num

	def get_reversible_num_1dir(self, x, y, dx, dy, mass_type):
		num = 0
		searching_x = x
		searching_y = y

		if self.mass_list[x][y].type != MassType.EMPTY:
			return 0

		opp_mass_type = Mass.get_opp_type(mass_type)

		while True:
			searching_x += dx
			searching_y += dy
			if 0 <= searching_x < Common.MASS_NUM and 0 <= searching_y < Common.MASS_NUM:
				if self.mass_list[searching_x][searching_y].type == mass_type:
					break
				elif self.mass_list[searching_x][searching_y].type == MassType.EMPTY:
					return 0
			else:
				return 0

		while True:
			searching_x -= dx
			searching_y -= dy
			if searching_x == x and searching_y == y:
				break
			else:
				num += 1
		return num

	def get_piece_num(self, mass_type):
		num = 0
		for i in range(8):
			for j in range(8):
				if self.mass_list[i][j].type == mass_type:
					num += 1
		return num

	def has_finished(self):
		for i in range(8):
			for j in range(8):
				if self.can_put(i, j, MassType.BLACK) or self.can_put(i, j, MassType.WHITE):
					return False
		return True


class Mass:

	def __init__(self, canvas, index_x, index_y):
		self.canvas = canvas
		self.id = 0
		self.index_x = index_x
		self.index_y = index_y
		self.type = MassType.EMPTY

		self.mass_size = 80
		self.piece_diameter = 70
		self.offset = (self.mass_size - self.piece_diameter) / 2

		self.mayumin = tk.PhotoImage(file='mayumin.gif')
		self.kanayan = tk.PhotoImage(file='kanayan.gif')
		#self.mayumin.subsample(10)
		#self.kanayan.subsample(10)
		#self.mayumin = Image.open('mayumin.png')
		#self.mayumin = ImageTk.PhotoImage(self.mayumin)
		#self.kanayan = Image.open('kanayan.png')
		#self.kanayan = ImageTk.PhotoImage(self.kanayan)

	@staticmethod
	def get_opp_type(mass_type):
		if mass_type == MassType.WHITE:
			return MassType.BLACK
		elif mass_type == MassType.BLACK:
			return MassType.WHITE
		else:
			return MassType.EMPTY

	def draw(self):
		color = ''
		if self.type == MassType.BLACK:
			color = 'Black'

		if self.type == MassType.WHITE:
			color = 'White'

		if self.id != 0:
			self.canvas.delete(self.id)

		if self.type != MassType.EMPTY:
			self.id = self.canvas.create_oval(self.index_x * self.mass_size + self.offset,
											  self.index_y * self.mass_size + self.offset,
											  self.index_x * self.mass_size + self.offset + self.piece_diameter,
											  self.index_y * self.mass_size + self.offset + self.piece_diameter,
											  fill=color)
			#if self.type == MassType.BLACK:
			#	self.id = self.canvas.create_image(self.index_x * self.mass_size + self.mass_size / 2,
			#									   self.index_y * self.mass_size + self.mass_size / 2,
			#									   #self.index_x * self.mass_size + self.mass_size,
			#									   #self.index_y * self.mass_size + self.mass_size,
			#									   image=self.mayumin)
			#elif self.type == MassType.WHITE:
			#	self.id = self.canvas.create_image(self.index_x * self.mass_size + self.mass_size / 2,
			#									   self.index_y * self.mass_size + self.mass_size / 2,
			#									   #self.index_x * self.mass_size + self.mass_size,
			#									   #self.index_y * self.mass_size + self.mass_size,
			#									   image=self.kanayan)

	def delete(self):
		if self.id != 0:
			self.canvas.delete(self.id)

	def delete_puttable(self):
		tag = 'puttable' + str(self.index_x) + str(self.index_y)
		self.canvas.delete(tag)

	def draw_puttable(self, puttable):
		tag = 'puttable' + str(self.index_x) + str(self.index_y)
		self.canvas.delete(tag)
		if puttable:
			self.canvas.create_rectangle(self.index_x * Common.MASS_SIZE,
										 self.index_y * Common.MASS_SIZE,
										 self.index_x * Common.MASS_SIZE + Common.MASS_SIZE,
										 self.index_y * Common.MASS_SIZE + Common.MASS_SIZE,
										 outline='Red', width=5,
										 tag=tag)



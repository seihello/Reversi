from Common import Common
from MassType import MassType
from Util import Util

class Board:

	def __init__(self):

		# 盤面を初期化
		self.mass_list = [[MassType.EMPTY] * Common.MASS_NUM for i in range(Common.MASS_NUM)]
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				self.mass_list[i][j] = MassType.EMPTY

		# 初期配置
		self.mass_list[3][3] = MassType.WHITE
		self.mass_list[3][4] = MassType.BLACK
		self.mass_list[4][3] = MassType.BLACK
		self.mass_list[4][4] = MassType.WHITE

	def update(self, x, y, mass_type):

		if Util.can_put(self.mass_list, x, y, mass_type):

			# 駒を配置
			self.mass_list[x][y] = mass_type

			# 駒をひっくり返す
			self.mass_list = Util.reverse(self.mass_list, x, y, mass_type)

			return True

		else:
			return False

	def has_finished(self):
		for i in range(Common.MASS_NUM):
			for j in range(Common.MASS_NUM):
				if Util.can_put(self.mass_list, i, j, MassType.BLACK) or Util.can_put(self.mass_list, i, j, MassType.WHITE):
					return False
		return True

	def get_puttable_list(self, mass_type):
		return Util.get_puttable_list(self.mass_list, mass_type)

	def can_put_somewhere(self, mass_type):
		return Util.can_put_somewhere(self.mass_list, mass_type)

	def get_piece_num(self, mass_type):
		return Util.get_piece_num(self.mass_list, mass_type)
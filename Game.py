from Board import *
from Common import Common
from GUI import GUI
from MassType import MassType
from Player import Player, PlayerType
from Strategy import StrategyType
from Util import Util

import pygame


class Game:

	def __init__(self, parent):

		self.root = parent
		self.gui = GUI(parent, self)

		self.players = {
			MassType.BLACK: Player(MassType.BLACK),
			MassType.WHITE: Player(MassType.WHITE),
		}

		self.start_app()

	def start_app(self):

		# BGMの再生を開始
		pygame.mixer.init()
		pygame.mixer.music.set_volume(0.10)
		self.bgm = pygame.mixer.Sound('bgm.wav')
		self.bgm.play(-1)

		# Top画面を表示
		self.gui.show_top()

	def start_game(self, black_player_type, white_player_type):

		# 盤面の描画をクリア
		self.gui.clear_board()

		# 盤面を初期化
		self.board = Board()

		# 黒が先手
		self.turn = MassType.BLACK

		# プレイヤータイプをセット
		self.players[MassType.BLACK].type = black_player_type
		self.players[MassType.WHITE].type = white_player_type

		# CPUが使用する駒配置アルゴリズムをセット
		if black_player_type == PlayerType.CPU:
			self.players[MassType.BLACK].set_strategy(StrategyType.EVALUATION_RANDOM)
		if white_player_type == PlayerType.CPU:
			self.players[MassType.WHITE].set_strategy(StrategyType.EVALUATION_THEN_FORECAST)

		# スコアを初期化
		self.players[MassType.BLACK].score = 2
		self.players[MassType.WHITE].score = 2

		# 盤面を描画
		self.gui.clear_latest_mass()
		self.update_board()

		# 先手がCPUの場合、駒配置を実行
		if self.players[self.turn].type == PlayerType.CPU:
			self.root.after(1000, self.cpu_put)

	def on_clicked_start_button(self):
		print('スタートボタン')

	def on_clicked_play_first_button(self):
		self.gui.show_game()
		self.start_game(PlayerType.HUMAN, PlayerType.CPU)

	def on_clicked_play_second_button(self):
		self.gui.show_game()
		self.start_game(PlayerType.CPU, PlayerType.HUMAN)

	def on_clicked_human_match_button(self):
		self.gui.show_game()
		self.start_game(PlayerType.HUMAN, PlayerType.HUMAN)

	def on_clicked_cpu_match_button(self):
		self.gui.show_game()
		self.start_game(PlayerType.CPU, PlayerType.CPU)

	def on_clicked_top_back_button(self):
		self.gui.show_top()

	def on_clicked_restart_button(self):
		self.start_game(self.players[MassType.BLACK].type, self.players[MassType.WHITE].type)

	def on_clicked_mass(self, event):

		# CPUのターンのクリックは無視
		if self.players[self.turn].type == PlayerType.CPU:
			return

		# クリックした座標からマスを算出
		x = event.x // Common.MASS_SIZE
		y = event.y // Common.MASS_SIZE

		# 駒を置く
		self.update(x, y)

	def cpu_put(self):
		mass_list_temp = Util.copy_mass_list(self.board.mass_list)
		x, y = self.players[self.turn].put(mass_list_temp)
		self.update(x, y)

	def update(self, x, y):
		if self.board.update(x, y, self.turn):

			# スコアを更新
			self.players[MassType.BLACK].score = self.board.get_piece_num(MassType.BLACK)
			self.players[MassType.WHITE].score = self.board.get_piece_num(MassType.WHITE)

			# ターン交代
			self.turn = Util.get_opp_type(self.turn)

			# GUIを更新
			self.gui.clear_latest_mass()
			self.gui.draw_latest_mass(x, y)
			self.update_board()

			# 終了した場合
			if self.board.has_finished():
				self.gui.show_result_dialog(self.players[MassType.BLACK].score,
											self.players[MassType.WHITE].score)
			# 終了していない場合
			else:
				# パスを判定
				if not self.board.can_put_somewhere(self.turn):
					self.turn = Util.get_opp_type(self.turn)
					self.gui.show_skip_dialog()

					# もう一度GUIを更新
					self.update_board()

				# CPUのターンならば一定時間経過後に駒を打つ
				if self.players[self.turn].type == PlayerType.CPU:
					self.root.after(1000, self.cpu_put)

	def update_board(self):
		self.gui.clear_board()
		self.gui.draw_board(self.board.mass_list,
							self.board.get_puttable_list(self.turn),
							self.players[MassType.BLACK].score,
							self.players[MassType.WHITE].score,
							self.turn)
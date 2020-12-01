import tkinter as tk
from MassType import MassType
from Board import *
from Player import Player, PlayerType
from BLabel import BLabel
from BButton import BButton
from Common import *
from tkinter import messagebox
import copy
from enum import Enum, auto
import playsound
import multiprocessing
import threading
import time
import pygame

# class GameType(Enum):




class Game:

	def __init__(self, parent):
		self.parent = parent
		# self.parent.wm_attributes("-transparentcolor", "Grey")

		self.top_frame = tk.Frame(self.parent, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='#006400')
		self.play_first_button = BButton(self.top_frame, text='先攻(黒)でスタート', font=("MSゴシック", "16", "bold"),
									   fg='Black', bg='Grey',
									   width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
									   command=self.on_clicked_play_first_button)
		self.play_first_button.place(x=(Common.WINDOW_WIDTH-Common.BUTTON_WIDTH)/2, y=200)

		self.play_second_button = BButton(self.top_frame, text='後攻(白)でスタート', font=("MSゴシック", "16", "bold"),
									   fg='Black', bg='Grey',
									   width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
									   command=self.on_clicked_play_second_button)
		self.play_second_button.place(x=(Common.WINDOW_WIDTH-Common.BUTTON_WIDTH)/2, y=400)

		# self.turn_select_frame = tk.Frame(self.parent, width=Common.window_width, height=Common.window_height, bg='Blue')


		self.game_frame = tk.Frame(self.parent, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='Grey')

		self.board_canvas = tk.Canvas(self.game_frame, width=Common.BOARD_WIDTH, height=Common.BOARD_HEIGHT,
									  highlightthickness=0, background='#006400')
		self.board_canvas.place(x=0, y=0)
		self.board_canvas.bind('<ButtonPress-1>', self.on_clicked_mass)

		# 得点表示画面の準備
		piece_offset_x = (Common.SCORE_WIDTH - Common.SCORE_PIECE_SIZE) // 2
		piece_offset_y = (Common.SCORE_HEIGHT // 2 - Common.SCORE_PIECE_SIZE) // 2

		self.black_score_canvas = tk.Canvas(self.game_frame, width=Common.SCORE_WIDTH, height=Common.SCORE_HEIGHT,
											highlightthickness=0, background='Red')
		self.black_score_canvas.place(x=Common.BOARD_WIDTH, y=0)
		self.black_score_canvas.create_oval(piece_offset_x,
											piece_offset_y,
											piece_offset_x + Common.SCORE_PIECE_SIZE,
											piece_offset_y + Common.SCORE_PIECE_SIZE,
											fill='Black', outline='White')
		self.black_score_label = BLabel(self.black_score_canvas,
										width=Common.SCORE_WIDTH - Common.TURN_BORDER_THICKNESS * 2,
										height=Common.SCORE_HEIGHT // 2 - Common.TURN_BORDER_THICKNESS,
										text='aa', fg='Black', bg='Red', font=("MSゴシック", "60", "bold"))
		self.black_score_label.place(x=Common.TURN_BORDER_THICKNESS, y=Common.SCORE_HEIGHT // 2)

		self.white_score_canvas = tk.Canvas(self.game_frame, width=Common.SCORE_WIDTH, height=Common.SCORE_HEIGHT,
											highlightthickness=0, background='Black')
		self.white_score_canvas.place(x=Common.BOARD_WIDTH, y=Common.SCORE_HEIGHT + Common.BUTTON_HEIGHT * 2)
		self.white_score_canvas.create_oval(piece_offset_x,
											piece_offset_y,
											piece_offset_x + Common.SCORE_PIECE_SIZE,
											piece_offset_y + Common.SCORE_PIECE_SIZE,
											fill='White', outline='White')
		self.white_score_label = BLabel(self.white_score_canvas,
										width=Common.SCORE_WIDTH - Common.TURN_BORDER_THICKNESS * 2,
										height=Common.SCORE_HEIGHT // 2 - Common.TURN_BORDER_THICKNESS,
										text='aa', fg='White', bg='Black', font=("MSゴシック", "60", "bold"))
		self.white_score_label.place(x=Common.TURN_BORDER_THICKNESS, y=Common.SCORE_HEIGHT // 2)

		self.top_back_button = BButton(self.game_frame, text='Topに戻る', font=("MSゴシック", "24", "bold"),
									   fg='Black', bg='Grey',
									   width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
									   command=self.on_clicked_top_back_button)
		self.top_back_button.place(x=Common.BOARD_WIDTH, y=Common.SCORE_HEIGHT)

		self.restart_button = BButton(self.game_frame, text='はじめから', font=("MSゴシック", "24", "bold"),
									  fg='Black', bg='Grey',
									  width=Common.BUTTON_WIDTH, height=Common.BUTTON_HEIGHT,
									  command=self.on_clicked_restart_button)
		self.restart_button.place(x=Common.BOARD_WIDTH, y=Common.SCORE_HEIGHT + Common.BUTTON_HEIGHT)

		self.score_canvas = {
			MassType.BLACK: self.black_score_canvas,
			MassType.WHITE: self.white_score_canvas,
		}

		self.score_labels = {
			MassType.BLACK: self.black_score_label,
			MassType.WHITE: self.white_score_label,
		}

		for i in range(9):
			self.board_canvas.create_line(80 * i, 0, 80 * i, 640, fill='White')
		for j in range(9):
			self.board_canvas.create_line(0, 80 * j, 640, 80 * j, fill='White')

		self.players = {
			MassType.BLACK: Player(MassType.BLACK),
			MassType.WHITE: Player(MassType.WHITE),
		}

		self.start_app()

		# self.start_button = tk.Button(self.game_frame, text='ゲーム開始', command=self.on_clicked_start_button)
		self.is_player_turn = False

	# self.header = tk.PhotoImage(file='header.gif')
	# self.header_canvas = tk.Canvas(parent, width=640, height=160, highlightthickness=0, background='#006400')
	# self.header_canvas.place(x=0, y=0)
	# self.header_canvas.create_image(320, 80, image=self.header)


	def start_app(self):

		# self.start_button.place(x=20, y=20)
		#self.parent.after(100, self.play_bgm_process)
		#self.parent.after(100, )
		#p = multiprocessing.Process(target=playsound.playsound, args=("yorunikakeru.mp3",))
		pygame.mixer.init()
		self.bgm = pygame.mixer.Sound('bgm.wav')
		self.bgm.play(100)
		self.top_frame.place(x=0, y=0)
		self.game_num = 0


	def start_game(self, black_player_type, white_player_type):

		self.turn = MassType.BLACK

		if self.game_num > 0:
			self.board.delete_pieces()
			self.board.delete_pieces()

		self.game_num += 1
		self.board = Board(self.board_canvas)

		self.players[MassType.BLACK].score = 2
		self.players[MassType.WHITE].score = 2
		self.players[MassType.BLACK].type = black_player_type
		self.players[MassType.WHITE].type = white_player_type

		self.score_labels[MassType.BLACK]['text'] = self.players[MassType.BLACK].score
		self.score_labels[MassType.WHITE]['text'] = self.players[MassType.WHITE].score
		# self.black_score_label.configure(text=self.players[MassType.BLACK].score)
		self.score_canvas[MassType.BLACK].create_rectangle(0, 0, Common.SCORE_WIDTH, Common.SCORE_HEIGHT,
														   outline='Blue', width=Common.TURN_BORDER_THICKNESS,
														   tag='turn_border')
		self.board.draw_pieces()
		self.board.draw_puttable(self.turn)

		if self.players[self.turn].type == PlayerType.CPU:
			self.parent.after(1000, self.cpu_put)

	def on_clicked_start_button(self):
		print('スタートボタン')

	def on_clicked_play_first_button(self):
		print('先攻ボタン')
		self.top_frame.place_forget()
		self.game_frame.place(x=0, y=0)
		self.start_game(PlayerType.HUMAN, PlayerType.CPU)

	def on_clicked_play_second_button(self):
		print('後攻ボタン')
		self.top_frame.place_forget()
		self.game_frame.place(x=0, y=0)
		self.start_game(PlayerType.CPU, PlayerType.HUMAN)

	def on_clicked_top_back_button(self):
		print('Topへ戻る')

	def on_clicked_restart_button(self):
		print('始めから')
		self.start_game(self.players[MassType.BLACK].type, self.players[MassType.WHITE].type)

	def on_clicked_mass(self, event):

		# CPUのターンのクリックは無視
		if self.players[self.turn].type == PlayerType.CPU:
			return

		# クリックした座標からマスを算出
		x = event.x // Common.MASS_SIZE
		y = event.y // Common.MASS_SIZE

		# 駒を置く
		self.player_put(x, y)

	def player_put(self, x, y):
		self.update(x, y)

	def cpu_put(self):
		print('CPU_PUT')
		for i in range(8):
			for j in range(8):
				if self.board.can_put(i, j, self.turn):
					self.update(i, j)
					return

	def update(self, i, j):
		if self.board.update(i, j, self.turn):
			self.update_player_score()
			self.board.draw_pieces()
			self.score_canvas[self.turn].delete('turn_border')

			# 終了判定
			if self.board.has_finished():
				black_num = self.board.get_piece_num(MassType.BLACK)
				while_num = self.board.get_piece_num(MassType.WHITE)
				if while_num < black_num:
					message = '黒の勝ちです'
				elif black_num < while_num:
					message = '白の勝ちです'
				else:
					message = '引き分けです'

				self.parent.after(200, lambda: messagebox.showinfo('ゲーム終了', message))

			else:
				self.turn = Mass.get_opp_type(self.turn)
				print(self.turn)
				if self.board.can_put_somewhere(self.turn):
					pass
				else:
					self.turn = Mass.get_opp_type(self.turn)
					self.parent.after(200, lambda: messagebox.showinfo('通知', '置く場所がないためパスします'))

				self.score_canvas[self.turn].create_rectangle(0, 0, Common.SCORE_WIDTH,
															  Common.SCORE_HEIGHT,
															  outline='Blue',
															  width=Common.TURN_BORDER_THICKNESS,
															  tag='turn_border')

				self.board.draw_puttable(self.turn)

				if self.players[self.turn].type == PlayerType.CPU:
					self.parent.after(1000, self.cpu_put)

	def update_player_score(self):
		self.players[MassType.BLACK].score = self.board.get_piece_num(MassType.BLACK)
		self.players[MassType.WHITE].score = self.board.get_piece_num(MassType.WHITE)

		# self.black_score_label.destroy()
		self.score_labels[MassType.BLACK]['text'] = self.players[MassType.BLACK].score
		self.score_labels[MassType.WHITE]['text'] = self.players[MassType.WHITE].score

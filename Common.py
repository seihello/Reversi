class Common:

	MASS_SIZE = 80
	MASS_NUM = 8
	BOARD_PIECE_SIZE = 70
	BOARD_WIDTH = MASS_SIZE * MASS_NUM
	BOARD_HEIGHT = MASS_SIZE * MASS_NUM

	SCORE_WIDTH = 160
	SCORE_HEIGHT = 240
	TURN_BORDER_THICKNESS = 10
	SCORE_PIECE_SIZE = 80

	WINDOW_WIDTH = BOARD_WIDTH + SCORE_WIDTH
	WINDOW_HEIGHT = BOARD_HEIGHT

	BUTTON_WIDTH = SCORE_WIDTH
	BUTTON_HEIGHT = (WINDOW_HEIGHT - (SCORE_HEIGHT * 2)) // 2

	TOP_BUTTON_WIDTH = WINDOW_WIDTH - 50 * 2
	TOP_BUTTON_FONT = ("MSゴシック", "24", "bold")


from enum import Enum, auto


class PlayerType(Enum):
	HUMAN = auto()
	CPU = auto()


class Player:

	def __init__(self, mass_type):
		self.mass_type = mass_type
		self.score = 2
		self.type = PlayerType.HUMAN

class Game(object):
	
	def __init__(self, board, mrX, detectives):
		""" Puts everything together
			and passes the board to every player.
		"""

		self.board = board
		self.mrX   = mrX
		self.detectives = detectives

		[player.setup(board, self) for player in [mrX] + detectives]

	def start(self):
		"""Launch the game"""
		pass

	def round(self):
		self.mrX.move()

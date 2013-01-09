"""
	Author: Alexander (dexter) Esselink

	Purpose: Model a game of Scotland Yard.

	Beginnings:
	    there is 1 mrX, and several detectives.
	    every player (mrX and the detectives) gets a starting position. 


"""

import json

class Player(object):
	identifiers = 0

	position = 0

	def __init__(self):
		self.id = "{}-{}".format(self.__class__.__name__, self.identifiers)
		Player.identifiers += 1
		self.tickets = self.tickets.copy()

	def __repr__(self):
		return self.id

	def setup(self, board, game):
		print "Setting board", self, board, game
		self.board = board
		self.game  = game

	def set_position(self, position):
		self.position = position

class Detective(Player):
	# initial tickets, will get copied (shallow)
	tickets = {
		'taxi'  : 10,
		'bus'   : 8,
		'metro' : 4
	}

class MrX(Player):
	# initial tickets, will get copied (shallow)
	tickets = {
		'taxi'   : 4,
		'bus'    : 3,
		'metro'  : 3,
		'double' : 2
	}


class Board(object):
	stops = []
	conn_metro = []
	conn_bus   = []
	conn_taxi  = []

	start_points = []

	def __init__(self, board_definition):
		self.stops = board_definition['stops']
		self.start_points = board_definition['start_points']

		self.conn_metro = board_definition['connections']['metro']
		self.conn_bus   = board_definition['connections']['bus']
		self.conn_taxi  = board_definition['connections']['taxi']

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

if __name__ == "__main__":
	n_detectives = 4

	mrX = MrX()
	detectives = [Detective() for i in range(n_detectives)]

	with open('london-subset.json') as board_definition:
		board_definition = json.loads(board_definition.read())

	board = Board(board_definition)

	game = Game(board, mrX, detectives)



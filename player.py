
class Player(object):
	identifiers = 0

	position = 0

	def __init__(self):
		self.id = "{0}-{1}".format(self.__class__.__name__, self.identifiers)
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

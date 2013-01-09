
class Player(object):
	identifiers = 0

	position = 0

	def __init__(self, game):
		self.id = "{0}-{1}".format(self.__class__.__name__, self.identifiers)
		
		Player.identifiers += 1
		self.tickets = self.tickets.copy()
		
		self.game = game

	def __repr__(self):
		return self.id

	def setup(self, game):
		print "Setting board", self, game
		self.game  = game

	def set_position(self, position):
		self.position = position
		print self, "setting position", position
		
	def move(self):
		print game.connected_stops(self.position)
		
#		res = raw_input("Moving {0} to ".format(self))
#		print res
		
		

class Detective(Player):
	# initial tickets, will get copied (shallow)
	tickets = {
		'taxi'  : 10,
		'bus'   : 8,
		'metro' : 4
	}
	
	def take_ticket(self, ticket_type):
		self.tickets[ticket_type] -= 1

class MrX(Player):
	# initial tickets, will get copied (shallow)
	tickets = {
		'taxi'   : 4,
		'bus'    : 3,
		'metro'  : 3,
		'double' : 2
	}
	
	revelation_moves = [3, 8, 13, 18]
	move_log = []
		
	def give_tickets(self, ticket_type, number_tickets):
		if ticket_type not in self.tickets:
			self.tickets[ticket_type] = number_tickets
		else:
			self.tickets[ticket_type] += number_tickets
	
	
	

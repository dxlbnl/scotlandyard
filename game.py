import random

class Game(object):
	
	def __init__(self, board):
		
		self.stops = board['stops']
		self.start_points = board['start_points']

		self.conn_metro = board['connections']['metro']
		self.conn_bus   = board['connections']['bus']
		self.conn_taxi  = board['connections']['taxi']


	def set_players(self, mrX, detectives):
		self.mrX = mrX
		self.detectives = detectives

	def start(self):
		"""Launch the game"""
		
		# assign a unique start position to all players
		players = [self.mrX] + self.detectives
		start_points = random.sample(self.start_points, len(players))
		[player.set_position(position) for player, position in zip(players, start_points)]
		
		# give mrX his black tickets
		self.mrX.give_tickets('black', len(self.detectives))

	def round(self):
		self.mrX.move()

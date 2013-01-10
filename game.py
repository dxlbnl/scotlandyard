import random

class Game(object):
	
	def __init__(self, board):
		
		self.stops = board['stops']
		self.start_points = board['start_points']

		self.connections = {
			'metro' : board['connections']['metro'],
			'bus'   : board['connections']['bus'],
			'taxi'  : board['connections']['taxi']
		}


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
		
		self.round()
		
	def connected_stops(self, position):
		return {
			type : [
					  connection[0] if position == connection[1] else connection[1]
						for connection in connections 
						if position in connection
					] 
			for type, connections in self.connections.iteritems()
		}
			

	def round(self):
		self.mrX.move()
		

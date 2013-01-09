

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



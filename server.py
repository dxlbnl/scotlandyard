from network import Server

class GameServer(Server):
	"""
		Handles json messages with a type field, 
		calling the method corresponding to handle_{type}.
	"""
	@classmethod
	def handle(type):
		"""Creates a handler factory, handlers take an id and data, and call the """

		def create_handler(self, id, data):
			pass
		pass

	authorized_tokens = ['HeldloWorld']

	def handle_login(self, id, data):
		print "Received data", id, data



		self.send(id, {
			"type"   : "login",
			"status" : "ok"
		})

	##############################
	##   Game Handling          ##
	##############################
	def handle_create_game(self, id, data):
		pass

	{
		"type"      : "login",
		"api_token" : "blabal"
	}


class Connection(object):
	def login(self, api_token):
		self.api_token = api_token


class APIHandler(object):
	def __init__(self, connection):
		self.connection = connection



	def login(self, api_token):
		print "Loggin in with", api_token


server = GameServer('dxtr.be')
server.launch()
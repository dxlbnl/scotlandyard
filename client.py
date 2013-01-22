from network.client import Client


class GameClient(Client):
	def __init__(self, *args, **kwargs):
		super(GameClient, self).__init__(*args, **kwargs)

	def login(self, api_token):
		print "Loggin in"
		self.server.login(api_token)

	def after_login(self, status):
		print "login", status

	def raise_error(self, msg):
		print "ERROR:", msg

	def game_created(self, game_id):
		print "SERVER: Game Created", game_id
		self.game_id = game_id

		self.register_player('mrX')
		self.register_player('detective')
		self.register_player('detective')

		self.server.start(self.game_id)



	def games_list(self, games_list):
		print games_list

	def player_registered(self, game_id, player_id, player_type):
		print "Player registered", game_id, player_id, player_type

	def register_player(self, player_type):
		self.server.game_register_player(self.game_id, player_type)

	def game_state(self, state):
		print "Game state"
		import pprint
		pprint.pprint(state)


if __name__ == "__main__":
	c = GameClient('dxtr.be', 9999)
	c.login('Hello World!')
	c.server.create_game()


	c.launch()	

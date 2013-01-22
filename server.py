from uuid import uuid4
import json

from network import Server, BaseHandler
from engine import Game

with open('newlondon.json') as board_file:
	board = json.loads(board_file.read())

class APIHandler(BaseHandler):
	authorized_tokens = ['Hello World!']

	games = {}


	def login(self, api_token):
		print "Loggin in with", api_token
		if api_token in self.authorized_tokens:
			self.client.after_login('ok')
		else:
			self.client.raise_error('Wrong api token')

	def create_game(self):
		game_id = str(uuid4())
		print "Game Created", game_id

		self.games[game_id] = Game(board)
		# TODO: Set owner for a game

		self.client.game_created(game_id)

	def list_games(self):
		self.client.games_list(self.games.keys())	

	def game_register_player(self, game_id, player_type):
		game = self.games[game_id]
		player_id = game.register_player(player_type, self.client)

		self.client.player_registered(game_id, player_id, player_type)

	def game_start(self, game_id):
		# TODO: only owner can start a game.
		game = self.games[game_id]
		game.start()

		game.send_state()

		game.round_state.next()

	def game_remove(self, game_id):
		# TODO: only owners can remove a game.

	def player_moved(self, game_id, player_id, location, transport):
		# TODO: only owners of that player can move.
		print "player moved", game_id, player_id, location
		game = self.games[game_id]

		game.move_player(player_id, location, transport)

	def send_board(self):
		print "Setting board"
		self.client.set_board(board)

		

if __name__ == "__main__":
	host = 'dxtr.be'
	port = 9999
	print "Launching server @ {}:{}".format(host, port)
	server = Server(APIHandler, host, port) 
	server.launch()

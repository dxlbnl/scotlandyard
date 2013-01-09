
"""
	Author: Alexander (dexter) Esselink

	Purpose: Model a game of Scotland Yard.

	Beginnings:
	    There is 1 mrX, and several detectives.
	    Every player (mrX and the detectives) gets a unique starting position. 
	    
	    Then, mrX makes a move, and in turn every detective makes a move.
	    Until mrX is caught, or the detectives don't have any tickets left.
        
        Every player can see 
"""

import json

from player import MrX, Detective
from game import Game

if __name__ == "__main__":
	n_detectives = 4

	with open('london-subset.json') as board_definition:
		board_definition = json.loads(board_definition.read())
	
	game = Game(board_definition)

	mrX = MrX(game)
	detectives = [Detective(game) for i in range(n_detectives)]

	game.set_players(mrX, detectives)
	
	game.start()


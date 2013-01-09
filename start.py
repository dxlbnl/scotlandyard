
"""
	Author: Alexander (dexter) Esselink

	Purpose: Model a game of Scotland Yard.

	Beginnings:
	    there is 1 mrX, and several detectives.
	    every player (mrX and the detectives) gets a unique starting position. 
	    
        
"""

import json

from player import MrX, Detective
from game import Game
from board import Board

if __name__ == "__main__":
	n_detectives = 4

	mrX = MrX()
	detectives = [Detective() for i in range(n_detectives)]

	with open('london-subset.json') as board_definition:
		board_definition = json.loads(board_definition.read())

	board = Board(board_definition)

	game = Game(board, mrX, detectives)



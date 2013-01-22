import random
from engine import MrX, Detective

class Game(object):
    
    def __init__(self, board):
        self.start_points = board['start_points']

        self.connections = board['connections']

        self.mrX = None
        self.detectives = []

        self.players = {}

	self.round_state = self.round()

    def register_player(self, type, client):
        if type == 'mrX':
            player = MrX(client)
            self.mrX = player
        elif type == 'detective':
            player = Detective(client)
            self.detectives.append(player)

        self.players[player.id] = player

        return player.id

    def start(self):
        """Launch the game"""
        
        # assign a unique start location to all players
        players = [self.mrX] + self.detectives
        start_points = random.sample(self.start_points, len(players))
        [player.set_location(location) for player, location in zip(players, start_points)]
         
        # give mrX his black tickets
        self.mrX.give_tickets('black', len(self.detectives))
        
    def reveal_mrX(self, location):
        print ">>> MrX is at {}".format(location)

    def won(self):
        return self.mrX.location in [detective.location for detective in self.detectives]

    def round(self):
        print "round..."

        # create a queue of actions to take place, they will be executed.
        yield self.mrX.move()

        for detective in self.detectives:
            yield detective.move()

        self.round_state = self.round()
        self.round_state.next()

        
        # assert location in self.connected_stops(self.mrX.location)[transport], "{} cannot travel to {} with {}.".format(self.mrX, location, transport)

        
    def move_player(self, player_id, location, transport):
        player = self.players[player_id]


        # Check if the player made a correct move.
        assert player.tickets[transport] != 0, "{} has no {} tickets left.".format(self.mrX, transport)

        self.players[player_id].set_location(location)
        self.send_state()

        try:
            self.round_state.next()
        except StopIteration:
            pass

    def send_state(self):
        state = {
            'detectives': [
                {
                    'id' : detective.id,
                    'location': detective.location,
                    'tickets': detective.tickets
                    # 'pastmoves': [int*]
                } for detective in self.detectives
            ],
            'MrX': {
                'id' : self.mrX.id,
                'location': self.mrX.location,
                'tickets': self.mrX.tickets,
                # 'log': [
                #     'card_type'*
                # ],
                # 'pastmoves': [int*]
            }
            # 'round': int,
            # 'turn' : int
        }
        clients = {player.client for player in [self.mrX] + self.detectives} 
        # sending state
        for client in clients:
            client.game_state(state)
        

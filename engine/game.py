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
        
        # assign a unique start location to all players
        players = [self.mrX] + self.detectives
        start_points = random.sample(self.start_points, len(players))
        [player.set_location(location) for player, location in zip(players, start_points)]
        
        # give mrX his black tickets
        self.mrX.give_tickets('black', len(self.detectives))
        
        while not self.won():
            self.round()

    def connected_stops(self, location):
        """Returns for every transport type the connected paths"""
        return {
            type : [
                      connection[0] if location == connection[1] else connection[1]
                        for connection in connections 
                        if location in connection
                    ] 
            for type, connections in self.connections.iteritems()
        }
    
    def reveal_mrX(self, location):
        print ">>> MrX is at {}".format(location)

    def won(self):
        return self.mrX.location in [detective.location for detective in self.detectives]

    def round(self):
        transport, location = self.mrX.move()

        assert self.mrX.tickets[transport] != 0, "{} has no {} tickets left.".format(self.mrX, transport)
        assert location in self.connected_stops(self.mrX.location)[transport], "{} cannot travel to {} with {}.".format(self.mrX, location, transport)

        self.mrX.log_move(transport, location)

        if self.won(): print "the detectives have won!"



        # for detective in self.detectives:
        #     detective.move()
        

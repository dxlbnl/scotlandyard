
class Player(object):
    identifiers = 0

    location = 0

    def __init__(self, client):
        self.id = "{0}-{1}".format(self.__class__.__name__, self.identifiers)
        
        Player.identifiers += 1
        self.tickets = self.tickets.copy()

        self.client = client
        
    def __repr__(self):
        return self.id

    def set_location(self, location):
        self.location = location
        print self, "setting location", location
        
    def move(self):
        print "Moving {}".format(self)

        # call the client to make the move.
        self.client.move(self.id)
        # print '\n'.join(("\t{}: {}".format(type, ', '.join(stop)) for type, stop in self.game.connected_stops(self.location).items()))
        
        # return raw_input("Moving {0} to ".format(self)).split(' ')
        
        

class Detective(Player):
    # initial tickets, will get copied (shallow)
    tickets = {
        'taxi'  : 10,
        'bus'   : 8,
        'metro' : 4
    }
    
    def take_ticket(self, ticket_type):
        self.tickets[ticket_type] -= 1

class MrX(Player):
    # initial tickets, will get copied (shallow)
    tickets = {
        'taxi'   : 4,
        'bus'    : 3,
        'metro'  : 3,
        'double' : 2
    }
    
    revelation_moves = [3, 8, 13, 18]
    move_log = []
        
    def give_tickets(self, ticket_type, number_tickets):
        if ticket_type not in self.tickets:
            self.tickets[ticket_type] = number_tickets
        else:
            self.tickets[ticket_type] += number_tickets
    
    def log_move(self, transport, location):
        print "Moving {} to {}".format(self, location)

        self.location = location
        self.move_log.append(transport)
        self.tickets[transport] -= 1

        if len(self.move_log) in self.revelation_moves:
            print "MRX: Revealing", self.location
    

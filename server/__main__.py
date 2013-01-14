
from tornado import ioloop, web
import json

from engine import Game, MrX, Detective


class MainHandler(web.RequestHandler):
    def get(self, te):
        self.render('board.html')

# class Game(object):


with open('london.json') as board_definition:
    board_definition = json.loads(board_definition.read())


class GameHandler(web.RequestHandler):
    games = []

    def get(self, action, id=None):
        if action == "create":
            id = len(self.games)

            
            n_detectives = 4
            game = Game(board_definition)

            mrX = MrX(game)
            detectives = [Detective(game) for i in range(n_detectives)]

            game.set_players(mrX, detectives)

            self.games.append(game)
            
            self.write(json.dumps({
                'id' : id,
                'board' : board_definition
            }))


application = web.Application([
    (r"/static/(.+)", web.StaticFileHandler, {"path": "server/static"}),
    (r"/game/(.*)/(.*)", GameHandler),
    (r"/frontend/(.*)", MainHandler),
], 
    debug = True,
    template_path = 'server/templates',
)

if __name__ == "__main__":
    print "Starting server"
    application.listen(8888)
    ioloop.IOLoop.instance().start()
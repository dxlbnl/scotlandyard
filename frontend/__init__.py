
from tornado import ioloop, web
import json

from engine import Game, MrX, Detective


class MainHandler(web.RequestHandler):
    def get(self, te):
        print "Client ({}) requested frontend.".format(self.request.remote_ip)
        self.render('board.html')

# class Game(object):


with open('london.json') as board_definition:
    board_definition = json.loads(board_definition.read())


class GameHandler(web.RequestHandler):
    games = []

    def write_json(self, data):
        self.write(json.dumps(data))

    def get(self):
        self.set_header("Content-Type", "application/json")

        self.write_json(dict(
            session_id = "12345"
        ))

        return

    def post(self):
        self.write_json('done')
        return

        if action == "create":
            id = len(self.games)

            
            n_detectives = 4
            game = Game(board_definition)

            detectives = [Detective(game) for i in range(n_detectives)]
            game.set_players(detectives=detectives)

            self.games.append(game)

            self.write(json.dumps({
                'id' : id,
                'board' : board_definition
            }))
        elif action == "list":
            self.write(json.dumps(range(len(self.games))))

    # def post(self, action, id):



application = web.Application([
    (r"/static/(.+)", web.StaticFileHandler, {"path": "server/static"}),
    (r"/game/?", GameHandler),
    (r"/frontend/?(.*)", MainHandler),
], 
    debug = True,
    template_path = 'server/templates',
)

# if __name__ == "__main__":
print "Starting server"
application.listen(8888)
ioloop.IOLoop.instance().start()
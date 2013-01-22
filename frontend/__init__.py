
from tornado import ioloop, web
import json

from engine import Game, MrX, Detective


class MainHandler(web.RequestHandler):
    def get(self):
        print "Client ({}) requested frontend.".format(self.request.remote_ip)
        self.render('board.html')



application = web.Application([
    (r"/static/(.+)", web.StaticFileHandler, {"path": "frontend/static"}),
    (r"/", MainHandler),
], 
    debug = True,
    template_path = 'frontend/templates',
)

# if __name__ == "__main__":
port = 8003
print "Starting server on", port
application.listen(port)
ioloop.IOLoop.instance().start()
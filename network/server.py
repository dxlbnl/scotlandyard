
import sys, inspect, traceback
import json
import asyncore, asynchat, socket

from functools import partial

from util import RPCObject

api_tokens = {
    'HelloWorld' : "Hoi, Dexter"
}

class Dispatcher(asyncore.dispatcher):
    """Dispatcher creates socket Connections and passes those to the server."""

    def __init__(self, server, host='localhost', port=8888):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))
        self.listen(1)

        self.server = server

    def handle_accept(self):
        # when we get a client connection start a dispatcher for that
        # client
        socket, address = self.accept()
        print 'Connection by', address

        self.server.connect(Connection(socket))

class Connection(asynchat.async_chat):

    on_message = None
    terminator = '\0'

    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock)
        self.ibuffer = ''
        self.set_terminator(self.terminator)

    def collect_incoming_data(self, data):
        """Buffer the data"""
        print "Collecting data",[data]
        self.ibuffer += data

    def found_terminator(self):
        try:
            if self.on_message:
                ibuffer = self.ibuffer
                self.ibuffer = ''

                self.on_message(ibuffer)
            self.ibuffer = ''
        except:
            traceback.print_exception(*sys.exc_info())

    def handle_close(self):
        print "Connection Closed"
        self.close()
        del self

    def push(self, msg):
        asynchat.async_chat.push(self, msg + self.terminator)

class Server(object):

    def __init__(self, Handler, host='localhost', port=8888):
        self.dispatcher = Dispatcher(self, host, port)
        self.connections = {}
        self.Handler = Handler

    def connect(self, connection):
        conn_id = id(connection)
        connection.on_message = partial(self.on_message, conn_id)

        self.connections[conn_id] = self.Handler(connection)

    def on_message(self, id, msg):
        print "got message", id, msg
        data = json.loads(msg)
        method = data.pop('method')

        if method[0] != '_': # dont allow the magic methods.
            # fetch the handler
            connection = self.connections[id]

            handler = getattr(connection, method, None)

            if handler:
                try:
                    handler(**data)
                except Exception, e:
                    print "Error in API method '{}' with {}".format(method, data)
                    raise e
            else:
                print "Did not find handler:", method, data
        else:
            print "Tried to use the magic methods"

    def launch(self):
        asyncore.loop()

    
class BaseHandler(object):
    __all__ = []

    def __init__(self, connection):
        self.__all__.append(connection)

        send = lambda data: connection.push(json.dumps(data))
        self.client = RPCObject(send)

        # set the api on the client.
        send({
            'method' : 'set_api',
            'api'    : self.get_api()
        })


    def set_api(self, api):
        print "Setting server API"
        self.client.api = api

    def get_api(self):
        print "Getting server API"
        """Returns all the allowed methods and possible arguments for the api"""
        getargs = lambda method: [arg for arg in inspect.getargspec(method).args + 
                                                 (inspect.getargspec(method).keywords or {}).keys()
                                            if arg != 'self'
                                ]
        methods = { 
            name :  getargs(method)
                for name, method in inspect.getmembers(self) 
                if name not in dir(BaseHandler) and inspect.ismethod(method)
        }

        return methods
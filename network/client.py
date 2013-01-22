import asyncore, asynchat, socket
import json
import sys, inspect, traceback

from util import RPCObject

class Dispatcher(asynchat.async_chat):
    count = 0
    terminator = "\0"

    on_message = None # callback

    def __init__(self, host='localhost', port=8888):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.set_terminator(self.terminator)

        self.connect((host, port))
        self.ibuffer = ''

    def push(self, msg):
        asynchat.async_chat.push(self, msg + self.terminator)

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer += data

    def found_terminator(self):
        """When the message is done, pass it on."""
        try:
            if self.on_message:
                self.on_message(self.ibuffer)
            self.ibuffer = ''
        except:
            traceback.print_exception(*sys.exc_info())

    def handle_close(self):
        print "Closing Connection"
        self.close()
        del self


class Client(object):
    """Manages incoming objects and return requests."""

    def __init__(self, host='localhost', port=8888):
        connection = Dispatcher(host, port)
        connection.on_message = self._on_message

        send = lambda data: connection.push(json.dumps(data))
        self.server = RPCObject(send)

        # set the api on the server.
        send({
            'method' : 'set_api',
            'api'    : self.get_api()
        })

        # self.server.set_api(api=self.get_api()) # notify the server of the api.

    def _on_message(self, msg):
        data = json.loads(msg)
        method = data.pop('method')

        if method[0] != '_': # dont allow the magic methods.
            # fetch the handler

            handler = getattr(self, method, None)

            if handler:
                self.server.__flush__() # make sure all messages are being sent to the server
                handler(**data)
            else:
                print "Did not find handler:", method, data
        else:
            print "Tried to use the magic methods"
    def close(self):
        self.connection.handle_close()

    def launch(self):
        asyncore.loop()

    def set_api(self, api):
        print "Setting server api in client"
        self.server.api = api
        self.server.__flush__()

    def get_api(self):
        print "Getting client api"
        """Returns all the allowed methods and possible arguments for the api"""
        getargs = lambda method: [arg for arg in inspect.getargspec(method).args + 
                                                 (inspect.getargspec(method).keywords or {}).keys()
                                            if arg != 'self'
                                ]
        methods = { 
            name :  getargs(method)
                for name, method in inspect.getmembers(self) 
                if name not in dir(Client) and inspect.ismethod(method)
        }

        return methods


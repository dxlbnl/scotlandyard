import asyncore, asynchat, socket
import json

class Server(asyncore.dispatcher):
    def __init__(self, host='localhost', port=8888, manager=None):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))
        self.listen(1)

        self.manager = manager

    def handle_accept(self):
        # when we get a client connection start a dispatcher for that
        # client
        socket, address = self.accept()
        print 'Connection by', address

        self.manager.connect(Connection(socket))

class Connection(asynchat.async_chat):

    on_message = None
    terminator = '\r\n'

    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock)
        self.ibuffer = ''
        self.set_terminator(self.terminator)

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer += data

    def found_terminator(self):
        if self.on_message:
            self.on_message(self.ibuffer)
        self.ibuffer = ''

    def handle_close(self):
        print "Connection Closed"
        self.close()
        del self

    def push(self, msg):
        msg += self.terminator
        asynchat.async_chat.push(self, msg)

from functools import partial

api_tokens = {
    'HelloWorld' : "Hoi, Dexter"
}

class Manager(object):

    def __init__(self):
        self.connections = {}

    def on_message(self, id, msg):
        data = json.loads(msg)

        handler = getattr(self, 'handle_{}'.format(data['type']))
        print handler
        if handler:
            handler(id, data)
        else:
            print "Did not find handler:", data['type'], data

    def send(self, id, data):
        self.connections[id].push(json.dumps(data))

    def connect(self, connection):
        conn_id = id(connection)
        connection.on_message = partial(self.on_message, conn_id)

        self.connections[conn_id] = connection
        print "Connection", conn_id, connection

    def handle_login(self, id, data):
        print "Login", id, data
        if 'api_token' in data and data['api_token'] in api_tokens:
            res = dict(
                type   = 'login',
                status = 'ok',
                greeting = api_tokens[data['api_token']]
            )
        else:
            res = {
                "type"   : 'login',
                "status" : "error",
                "error"  : 'invalid api token'
            }

        self.send(id, res)



m = Manager()
s = Server('194.145.201.129', manager=m)


asyncore.loop()
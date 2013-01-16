
import sys, traceback
import json
import asyncore, asynchat, socket

from functools import partial

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
    terminator = '\r\n'

    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock)
        self.ibuffer = ''
        self.set_terminator(self.terminator)

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer += data

    def found_terminator(self):
        try:
            if self.on_message:
                self.on_message(self.ibuffer)
            self.ibuffer = ''
        except:
            traceback.print_exception(*sys.exc_info())

    def handle_close(self):
        print "Connection Closed"
        self.close()
        del self

    def push(self, msg):
        msg += self.terminator
        asynchat.async_chat.push(self, msg)


class Server(object):

    def __init__(self, host='localhost', port=8888):
        self.dispatcher = Dispatcher(self, host, port)
        self.connections = {}

    def set_handler(self, handler):
        

    def on_message(self, id, msg):
        data = json.loads(msg)

        handler = getattr(self, 'handle_{type}'.format(type=data['type']))

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



    def launch(self):
        asyncore.loop()


# class MessageHandler(object):
    # """handles messages"""        

import asyncore, asynchat, socket
import json

requests = {
    "login" : {
        "type"      : "login",
        "api_token" : "HeldloWorld"
    }
}


class Client(asynchat.async_chat):
    count = 0
    terminator = "\r\n"

    on_message = None # callback

    def __init__(self, host='localhost', port=8888):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.set_terminator(self.terminator)

        self.connect((host, port))
        self.ibuffer = ''

    def push(self, msg):
        msg += self.terminator
        asynchat.async_chat.push(self, msg)

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer += data

    def found_terminator(self):
        print "Hier"
        if self.on_message:
            self.on_message(self.ibuffer)
        self.ibuffer = ''

    def handle_close(self):
        print "Closing Connection"
        self.close()
        del self

class Manager(object):
    """Manages incoming objects and return requests."""

    def __init__(self, connection):
        self.connection = connection
        self.connection.on_message = self.handle_msg

    def send(self, data):
        self.connection.push(json.dumps(data))

    def handle_msg(self, msg):
        print "Got msg", json.loads(msg)
        self.connection.handle_close()





c = Manager(Client('dxtr.be'))

c.send(requests['login'])


asyncore.loop()

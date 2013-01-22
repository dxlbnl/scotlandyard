
from collections import deque
import json

class RPCProducer(object):
    def __init__(self, terminator_string):
        self.__data = deque()
        self.__terminator_string = terminator_string

    def more(self):
        print "Asking for more"

    def append(self, data):
        print "Appending data", data
        self.__data.append(data)

    def __getitem__(self, item):
        print "Getting item", item
        if item in self.__data:
            return json.dumps(self.__data[item]) + self.__terminator_string
        return ''

    def __delitem__(self, item):
        print "Deleteing item", item
        del self.__data[item]

    def __getattr__(self, name):
        print "Getting thing", name
        raise ValueError

    def __nonzero__(self):
        if self.__data:
            return True
        return False


class RPCProducer(deque):
    def __init__(self, terminator_string):
        super(RPCProducer, self).__init__()

    def more(self):
        print "Asking for more"

    def append(self, data):
        print "Appending data", data
        return super(RPCProducer, self).append(data)

    def __getitem__(self, item):
        print "Getting item", item
        return super(RPCProducer, self).__getitem__(item)

    def __delitem__(self, item):
        print "Deleteing item", item
        return super(RPCProducer, self).__delitem__(item)

    def __nonzero__(self):
        return True

    # def __getattr__(self, name):
        # print "Getting thing", name
        # raise ValueError
RPCProducer = deque

class RPCObject(object):
    """Captures method requests, and packages them as remote procedure calls."""

    def __init__(self, send):
        self.__send = send
        self.api = {}
        self.__queue = deque()

    def __flush__(self):
        if self.api:
            while self.__queue:
                msg = self.__queue.popleft()
                if msg['method'] in self.api:
                    self.__send__(**msg)
                else:
                    break

    def __send__(self, method, args, kwargs):
        data = {'method' : method}
        data.update(dict(zip(self.api[method], args)))
        data.update(kwargs)
        self.__send(data)
            


    def __getattr__(self, name):
        method = name

        def function(*args, **kwargs):
            if self.api:
                self.__flush__()
                self.__send__(method, args, kwargs)
            else:
                self.__queue.append(dict(method=method, args=args, kwargs=kwargs))
                print " :: Adding '{}' to the queue, UNKNOWN METHOD.".format(method)


        return function

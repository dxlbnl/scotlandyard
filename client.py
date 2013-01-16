from network.client import Client


requests = {
    "login" : {
        "type"      : "login",
        "api_token" : "HeldloWorld"
    }
}



class GameClient(Client):
	def __init__(self, host='localhost', port=8888):
		super(GameClient, self).__init__(host, port)
		print "Sending"
		self.send(requests['login'])



c = GameClient('dxtr.be')
c.launch()
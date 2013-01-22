import json

with open('london.json') as f:
	definition = json.loads(f.read())
	connections = definition['connections']
	start_points = definition['start_points']
	stops = definition['stops']


with open('newlondon.json', 'w') as f:
	f.write(json.dumps({
		'connections' : {
				stop : {
					transport : [conn[0] if stop == conn[1] else conn[1]
			                        for conn in conns 
			                        if stop in conn]
					for transport, conns in connections.iteritems()
				}
				for stop in stops
			},
		'start_points' : start_points
		}, indent=4, sort_keys=True))

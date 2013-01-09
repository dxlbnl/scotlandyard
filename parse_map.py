
import re
import json
from lxml import etree
from functools import partial
from pprint import pprint, pformat

class Stop(object):
    bus = False
    metro = False

    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return "{:5} at {:10}".format(
            "Metro" if self.metro else "Bus" if self.bus else "Taxi",
            self.pos
        )

def get_position(path):
    regex = re.compile('.+\((.+)\)')
    transform = path.get('transform')
    if transform:
        transform = regex.findall(transform)[0].split(',')

        return tuple(map(int, map(float, transform)))
    return (0,0)

add_pos   = lambda pos1, pos2: tuple(map(sum, zip(pos1, pos2)))
add_stop   = lambda pos1, (id, pos): (id, add_pos(pos1, pos))

def parse_stop(stop):
    cx = "{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cx"
    cy = "{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cy"

    pos = tuple(map(float, (stop.get(cx), stop.get(cy))))
    return (stop.get('id'), add_pos(pos, get_position(stop)))

def parse_line(line):
    d = line.get('d')
    path_type = d[0]

    points = d[2:].split(' ')
    assert len(points) == 2

    l_from, l_diff = map(lambda point: tuple(map(float, point.split(','))), points)
    if path_type == "M": #absolute
        l_to = l_diff
    else:
        l_to = add_pos(l_from, l_diff)

    return tuple(map(partial(add_pos, get_position(line)), (l_from, l_to)))


# SVG Parsing functions.
namespaces = {
    'inkscape' : 'http://www.inkscape.org/namespaces/inkscape', 
    'svg'      : 'http://www.w3.org/2000/svg',
    'sodipodi' : "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
}

get_layer = lambda root, label: root.xpath('svg:g[@inkscape:label = "{}"]'.format(label), namespaces=namespaces)[0]
get_stops = lambda layer: layer.xpath('svg:path[@sodipodi:type = "arc"]', namespaces=namespaces)
get_lines = lambda layer: layer.xpath('svg:path[not(@sodipodi:type)]', namespaces=namespaces)

def matching_stops(l1, l2):
    range = 30
    i = 0

    cnt = 0
    for m_id, (mx, my) in l1:
        for b_id, (bx, by) in l2:
            if ((bx - range < mx < bx + range)
                and
               (by - range < my < by + range)):
                i += 1

                cnt += 1
                yield b_id
                break

def matching_lines(lines, stops):
    for line in lines:
        matches = tuple(matching_stops(line, stops))
        if len(matches) != 2:
            print "ERROR", matches, line
        yield matches



if __name__ == "__main__":
    map_file = 'london.svg'

    out_file = "london.json"

    with open(map_file) as map_file:
        tree = etree.parse(map_file)

        root = tree.getroot()
        # find all layers.
        groups = root.xpath("svg:g", namespaces=namespaces)

        taxi_layer  = get_layer(root, 'Taxi')
        bus_layer   = get_layer(root, 'Bus')
        metro_layer = get_layer(root, 'Metro')

        taxi_stops  = get_stops(taxi_layer)
        bus_stops   = get_stops(bus_layer)
        metro_stops = get_stops(metro_layer)

        taxi_position = get_position(taxi_layer)
        bus_position = get_position(bus_layer)
        metro_position = get_position(metro_layer)

        m_pos = map(partial(add_stop, metro_position), 
                    map(parse_stop, metro_stops)
                )
        b_pos = map(partial(add_stop, bus_position),   
                    map(parse_stop, bus_stops)
                )
        t_pos = map(partial(add_stop, taxi_position),  
                    map(parse_stop, taxi_stops)
                )

        metro_lines = [map(
            lambda p: ('line', add_pos(metro_position, p)), 
            parse_line(line)
        ) for line in get_lines(metro_layer)]
        bus_lines = [map(
            lambda p: ('line', add_pos(bus_position, p)), 
            parse_line(line)
        ) for line in get_lines(bus_layer)]
        taxi_lines = [map(
            lambda p: ('line', add_pos(taxi_position, p)), 
            parse_line(line)
        ) for line in get_lines(taxi_layer)]

        stops = {
            id : Stop(pos) for id, pos in t_pos
        }

        for stop in matching_stops(m_pos, t_pos):
            stops[stop].metro = True

        for stop in matching_stops(b_pos, t_pos):
            stops[stop].bus = True

        metro_connections = list(matching_lines(metro_lines, t_pos))
        bus_connections   = list(matching_lines(bus_lines, t_pos))
        taxi_connections  = list(matching_lines(taxi_lines, t_pos))

    with open(out_file, 'w') as out_file:
        out_file.write(json.dumps({
            'stops' : stops.keys(),
            'connections' : {
                'metro' : metro_connections,
                'bus'   : bus_connections,
                'taxi'  : taxi_connections
            }, 
            "start_points" : ["199", "188", "108", "162", "141", "186", "136", "117"]
        },indent = 4))


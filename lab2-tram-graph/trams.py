import sys
import json

sys.path.append('../lab1-group-148')

import tramdata as td
from graphs import WeightedGraph, view_shortest, dijkstra


TRAM_FILE = '../lab1-group-148/tramnetwork.json'


class TramNetwork(WeightedGraph):
    def __init__(self, tramdict):
        # tramdict: the dictionary loaded from tramnetwork.json
        super().__init__()

        self.tramdict = tramdict
        self.stopdict = tramdict["stops"]
        self.linedict = tramdict["lines"]
        self.timedict = tramdict["times"]

        # Build the graph structure:    
        for stop_name, info in self.stopdict.items():
            self.add_vertex(stop_name)
            self.set_vertex_value(stop_name, info)

        # create edges between adjacent stops and set weights
        for line, stops in self.linedict.items():
            for s1, s2 in zip(stops, stops[1:]):
                a, b = sorted([s1, s2])
                minutes = self.timedict[a][b]

                # If the edge already exists, take the smaller time
                existing = self.get_weight(s1, s2)
                if existing is None or minutes < existing:
                    self.set_weight(s1, s2, minutes)


    def position(self, stop):
        # Return (lat, lon) as floats for a given stop.
        info = self.stopdict[stop]
        lat_str, lon_str = info["position"]
        return float(lat_str), float(lon_str)

    def transition_time(self, stop1, stop2):
        # Returns None if there is no direct edge.
        if not self.has_edge(stop1, stop2):
            return None
        a, b = sorted([stop1, stop2])
        return self.timedict[a][b]

    def geo_distance(self, stop1, stop2):
        # Geographic distance in km, reusing Lab1 distance_between_stops().
        return td.distance_between_stops(self.stopdict, stop1, stop2)

    def lines_via_stop(self, stop):
        # List all line numbers (strings) that pass this stop, sorted numerically.
        result = []
        for line, stops in self.linedict.items():
            if stop in stops:
                result.append(line)
        result.sort(key=int)
        return result

    def stops_on_line(self, line):
        # Return list of stops on a given line.
        return list(self.linedict[line])

    def all_stops(self):
        # Return all stop names, sorted.
        return sorted(self.stopdict.keys())

    def all_lines(self):
        # Return all line numbers, sorted numerically.
        return sorted(self.linedict.keys(), key=int)

    def extreme_position(self):
        # Return (min_lat, max_lat, min_lon, max_lon) over all stops.
        lats = []
        lons = []
        for stop in self.stopdict:
            lat, lon = self.position(stop)
            lats.append(lat)
            lons.append(lon)
        return min(lats), max(lats), min(lons), max(lons)



def readTramNetwork(tramfile=TRAM_FILE):
    # Read tram network JSON file and return a TramNetwork instance.
    with open(tramfile, encoding='utf-8') as f:
        tramdict = json.load(f)
    return TramNetwork(tramdict)

def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')
    view_shortest(G, a, b)


def demo_fastest_time():
    # Show fastest route (by time)
    G = readTramNetwork()
    source = "Chalmers"
    target = "Järntorget"

    paths = dijkstra(G, source, cost=lambda u, v: G.get_weight(u, v))
    path = paths[target]
    minutes = sum(G.get_weight(a, b) for a, b in zip(path, path[1:]))

    print("Fastest-time path from", source, "to", target, ":", path)
    print("Total minutes:", minutes)



if __name__ == '__main__':
    demo()

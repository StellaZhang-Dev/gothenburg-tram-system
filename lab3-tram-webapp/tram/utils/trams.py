import json
import math
import os
from .graphs import WeightedGraph
from django.conf import settings


# Load tramnetwork.json from Lab 1
# TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')
TRAM_FILE = os.path.join(settings.BASE_DIR, "static", "tramnetwork.json")

class TramNetwork(WeightedGraph):

    def __init__(self, tramdict):
        super().__init__()

        self.tramdict = tramdict
        self.stopdict = tramdict["stops"]
        self.linedict = tramdict["lines"]
        self.timedict = tramdict["times"]

        # Add all stops as vertices
        for stop_name, info in self.stopdict.items():
            self.add_vertex(stop_name)
            self.set_vertex_value(stop_name, info)

        # Add edges between adjacent stops
        for line, stops in self.linedict.items():
            for s1, s2 in zip(stops, stops[1:]):
                a, b = sorted([s1, s2])
                minutes = self.timedict[a][b]

                # If the edge already exists, keep the smallest value
                old = self.get_weight(s1, s2)
                if old is None or minutes < old:
                    self.set_weight(s1, s2, minutes)          


    def position(self, stop):
        # Return (lat, lon) as floats.
        lat_str, lon_str = self.stopdict[stop]["position"]
        return float(lat_str), float(lon_str)

    def transition_time(self, stop1, stop2):
        # Return travel time in minutes, or None if not adjacent.
        if not self.has_edge(stop1, stop2):
            return None
        a, b = sorted([stop1, stop2])
        return self.timedict[a][b]

    def geo_distance(self, stop1, stop2):
        # Return geographic distance in kilometers.
        lat1, lon1 = self.position(stop1)
        lat2, lon2 = self.position(stop2)

        R = 6371.0  # Earth radius

        p1 = math.radians(lat1)
        p2 = math.radians(lat2)
        dp = math.radians(lat2 - lat1)
        dl = math.radians(lon2 - lon1)

        a = (
            math.sin(dp / 2) ** 2
            + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def lines_via_stop(self, stop):
        # Return all line numbers passing this stop.
        result = [line for line, stops in self.linedict.items() if stop in stops]
        return sorted(result, key=int)

    def stops_on_line(self, line):
        # Return all stops on a line.
        return list(self.linedict[line])

    def all_stops(self):
        # Return all stop names, sorted.
        return sorted(self.stopdict.keys())

    def all_lines(self):
        # Return all line numbers, sorted.
        return sorted(self.linedict.keys(), key=int)

    def extreme_positions(self):
        # Return (min_lon, min_lat, max_lon, max_lat).
        # Used by tramviz.py for drawing.
        lats = []
        lons = []
        for stop in self.stopdict:
            lat, lon = self.position(stop)
            lats.append(lat)
            lons.append(lon)
        return min(lons), min(lats), max(lons), max(lats)
    
    def resolve_stop_name(self, raw):
        # exact key
        if raw in self.stopdict:
            return raw

        norm = normalize_stop_name(raw)

        # exact normalized matches
        exact_matches = []
        for real in self.stopdict.keys():
            if normalize_stop_name(real) == norm:
                exact_matches.append(real)

        if len(exact_matches) == 1:
            return exact_matches[0]

        # substring matches
        substring_matches = []
        for real in self.stopdict.keys():
            if norm in normalize_stop_name(real):
                substring_matches.append(real)

        if len(substring_matches) == 1:
            return substring_matches[0]

        return None


def normalize_stop_name(name):
    
    # Lowercase a stop name and replace å/ä/ö with a/o for matching.
    s = name.strip().lower()
    s = s.replace("å", "a").replace("ä", "a").replace("ö", "o")
    return s


def readTramNetwork():
    # Read tramnetwork.json and return a TramNetwork object.
    with open(TRAM_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return TramNetwork(data)


def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # No extra time for line changes
    t = spec_network.transition_time(a, b)
    return t


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # No extra distance for line changes
    return spec_network.geo_distance(a, b)


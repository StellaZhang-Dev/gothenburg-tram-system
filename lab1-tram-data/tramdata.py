# Lab 1 – Tram data processing (submission version)

import sys
import json
import math

# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'

# file to give
TRAM_FILE = './tramnetwork.json'



def build_tram_stops(jsonobject):

    # Return the stops dictionary
    return jsonobject



def build_tram_lines(lines):

    # Build line and time dictionaries
    linedict = {}
    timedict = {}

    current_line = None   
    prev_stop = None      
    prev_minutes = None   

    for raw in lines:
        
        line = raw.rstrip("\n")

        if not line.strip():
            prev_stop = None
            prev_minutes = None
            continue

        stripped = line.strip()

        if stripped.endswith(":"):
            # new line number
            current_line = stripped[:-1].strip()  
            linedict[current_line] = []
            prev_stop = None
            prev_minutes = None
            continue

        stop_part, time_part = line.rstrip().rsplit(" ", 1)
        stop_name = stop_part.rstrip()
        time_str = time_part.strip()  

        hour, minute = map(int, time_str.split(":"))
        total_minutes = hour * 60 + minute

        if current_line is None:
            raise ValueError("Stop found before line number.")
        linedict[current_line].append(stop_name)

        if prev_stop is not None:
            delta = total_minutes - prev_minutes

            a, b = sorted([prev_stop, stop_name])
            if a not in timedict:
                timedict[a] = {}
            if b not in timedict[a]:
                timedict[a][b] = delta

        prev_stop = stop_name
        prev_minutes = total_minutes

    return linedict, timedict



def build_tram_network(stopfile, linefile):
    
    with open(stopfile, encoding="utf-8") as f:
        raw_stops = json.load(f)
    stopdict = build_tram_stops(raw_stops)

    with open(linefile, encoding="utf-8") as f:
        lines = f.readlines()
    linedict, timedict = build_tram_lines(lines)

    tramdict = {
        "stops": stopdict,
        "lines": linedict,
        "times": timedict,
    }

    with open(TRAM_FILE, "w", encoding="utf-8") as f:
        json.dump(tramdict, f, ensure_ascii=False, indent=2)

    return tramdict



def lines_via_stop(linedict, stop):

    # Return all lines that pass the given stop
    result = []

    for line, stops in linedict.items():
        if stop in stops:
            result.append(line)

    result.sort(key=int)
    return result



def lines_between_stops(linedict, stop1, stop2):
    result = []

    for line, stops in linedict.items():
        if stop1 in stops and stop2 in stops:
            result.append(line)

    result.sort(key=int)
    return result



def time_between_stops(linedict, timedict, line, stop1, stop2):

    # check that the line exists
    if line not in linedict:
        print("unknown line")
        return None

    stops = linedict[line]

    # both stops must be on this line
    if stop1 not in stops or stop2 not in stops:
        print("stops not on this line")
        return None

    # same stop: zero time
    if stop1 == stop2:
        return 0

    # find positions of the stops
    i1 = stops.index(stop1)
    i2 = stops.index(stop2)

    # go from earlier index to later index
    start = min(i1, i2)
    end = max(i1, i2)

    total = 0

    # walk through all neighbour pairs between stop1 and stop2
    for i in range(start, end):
        s1 = stops[i]
        s2 = stops[i + 1]

        a, b = sorted([s1, s2])

        try:
            delta = timedict[a][b]
        except KeyError:
            print("no time data between", s1, "and", s2)
            return None

        total += delta

    return total



def distance_between_stops(stopdict, stop1, stop2):
    if stop1 not in stopdict or stop2 not in stopdict:
        print("unknown stop")
        return None

    def get_lat_lon(name):
        info = stopdict[name]

        if "position" not in info or len(info["position"]) != 2:
            raise ValueError(f"Bad position data for stop: {name} -> {info}")
        lat_str, lon_str = info["position"]
        return float(lat_str), float(lon_str)

    lat1, lon1 = get_lat_lon(stop1)
    lat2, lon2 = get_lat_lon(stop2)

    # Haversine formula
    R = 6371.0  # Earth radius

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c

    return round(distance_km, 3)



# extra feature 1
def normalize_stop_name(name):
    # Lowercase and replace Swedish letters
    s = name.strip().lower()
    s = s.replace("å", "a").replace("ä", "a").replace("ö", "o")
    return s



# extra feature 2
def resolve_stop_name(stopdict, raw):
    # Return the real stop name if it matches case/åäö-insensitive
    if raw in stopdict:
        return raw

    norm = normalize_stop_name(raw)

    exact_matches = []
    for real in stopdict.keys():
        if normalize_stop_name(real) == norm:
            exact_matches.append(real)

    if len(exact_matches) == 1:
        return exact_matches[0]

    substring_matches = []
    for real in stopdict.keys():
        if norm in normalize_stop_name(real):
            substring_matches.append(real)

    if len(substring_matches) == 1:
        return substring_matches[0]

    return None



def answer_query(tramdict, query):

    # Parse a query string and return the answer value
    stopdict = tramdict["stops"]
    linedict = tramdict["lines"]
    timedict = tramdict["times"]

    q = query.strip()
    ql = q.lower()

    # via <stop>
    if ql.startswith("via "):
        raw_stop = q[4:].strip()
        stop = resolve_stop_name(stopdict, raw_stop)
        if stop is None:
            return "unknown arguments"
        return lines_via_stop(linedict, stop)

    # between <stop1> and <stop2>
    if ql.startswith("between "):
        and_pos = ql.find(" and ")
        if and_pos == -1:
            return "sorry, try again"

        raw_stop1 = q[len("between "):and_pos].strip()
        raw_stop2 = q[and_pos + len(" and "):].strip()

        stop1 = resolve_stop_name(stopdict, raw_stop1)
        stop2 = resolve_stop_name(stopdict, raw_stop2)

        if stop1 is None or stop2 is None:
            return "unknown arguments"
        return lines_between_stops(linedict, stop1, stop2)

    # time with <line> from <stop1> to <stop2>
    if ql.startswith("time with "):
        rest = q[len("time with "):]
        rest_l = rest.lower()

        from_pos = rest_l.find(" from ")
        if from_pos == -1:
            return "sorry, try again"

        line = rest[:from_pos].strip()
        rest2 = rest[from_pos + len(" from "):]
        rest2_l = rest2.lower()

        to_pos = rest2_l.find(" to ")
        if to_pos == -1:
            return "sorry, try again"

        raw_stop1 = rest2[:to_pos].strip()
        raw_stop2 = rest2[to_pos + len(" to "):].strip()

        stop1 = resolve_stop_name(stopdict, raw_stop1)
        stop2 = resolve_stop_name(stopdict, raw_stop2)

        if line not in linedict or stop1 is None or stop2 is None:
            return "unknown arguments"

        t = time_between_stops(linedict, timedict, line, stop1, stop2)
        if t is None:
            return "unknown arguments"
        return t

    # distance from <stop1> to <stop2>
    if ql.startswith("distance from "):
        rest = q[len("distance from "):]
        rest_l = rest.lower()

        to_pos = rest_l.find(" to ")
        if to_pos == -1:
            return "sorry, try again"

        raw_stop1 = rest[:to_pos].strip()
        raw_stop2 = rest[to_pos + len(" to "):].strip()

        stop1 = resolve_stop_name(stopdict, raw_stop1)
        stop2 = resolve_stop_name(stopdict, raw_stop2)

        if stop1 is None or stop2 is None:
            return "unknown arguments"

        d = distance_between_stops(stopdict, stop1, stop2)
        if d is None:
            return "unknown arguments"
        return d

    # other
    return "sorry, try again"



def dialogue(tramfile=TRAM_FILE):
    with open(tramfile, encoding="utf-8") as f:
        tramdict = json.load(f)

    while True:
        try:
            line = input("> ")
        except EOFError:
            break

        query = line.strip()

        if not query:
            continue

        if query == "quit":
            break

        answer = answer_query(tramdict, query)

        if answer == "sorry, try again":
            print("sorry, try again")
        elif answer == "unknown arguments":
            print("unknown arguments")
        elif answer is None:
            
            print("sorry, try again")
        else:
            print(answer)



if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()
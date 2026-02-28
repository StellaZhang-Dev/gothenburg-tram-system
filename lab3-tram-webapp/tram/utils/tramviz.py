# visualization of shortest path in Lab 3, modified to work with Django

from .trams import (
    readTramNetwork,
    specialize_stops_to_lines,
    specialized_transition_time,
    specialized_geo_distance,
)
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings
from django.core.files.storage import default_storage

def show_shortest(dep, dest):
    network = readTramNetwork()
    
    # resolve user-typed names to real stop names
    real_dep = network.resolve_stop_name(dep)
    real_dest = network.resolve_stop_name(dest)

    # if cannot resolve, show a message and keep map uncoloured
    if real_dep is None or real_dest is None:
        bad = dep if real_dep is None else dest
        time_text = f"Unknown stop name: {bad}"
        dist_text = ""
        
        # just return the base image without extra colours
        infile = os.path.join(
            settings.BASE_DIR,
            'tram/templates/tram/images/gbg_tramnet.svg'
        )

        # still generate a copy in generated/, so the template has a file
        dep_safe = default_storage.get_valid_name(dep)
        dest_safe = default_storage.get_valid_name(dest)
        outfile_unique_name = f"shortest_path_{dep_safe}_{dest_safe}.svg"
        outfile = os.path.join(
            settings.BASE_DIR,
            f'tram/templates/tram/images/generated/{outfile_unique_name}'
        )
        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        # color with all white (no special stops)
        def colors(_):
            return "white"

        color_svg_network(infile, outfile, colormap=colors)
        return time_text, dist_text, outfile

    # Specialise stops to (stop, line) graph
    spec_network = specialize_stops_to_lines(network)

    # Quickest path (by time)
    paths_time = dijkstra(
        spec_network,
        real_dep,
        cost=lambda a, b: specialized_transition_time(spec_network, a, b)
    )
    quickest = paths_time.get(real_dest, [])

    # compute total travel time
    total_minutes = 0
    for a, b in zip(quickest, quickest[1:]):
        t = specialized_transition_time(spec_network, a, b)
        if t:
            total_minutes += t

    # Shortest path (by geographic distance)
    paths_geo = dijkstra(
        spec_network,
        real_dep,
        cost=lambda a, b: specialized_geo_distance(spec_network, a, b)
    )
    shortest = paths_geo.get(real_dest, [])

    # compute total km
    total_km = 0.0
    for a, b in zip(shortest, shortest[1:]):
        total_km += specialized_geo_distance(spec_network, a, b)


    # build output texts
    time_text = (
        "Quickest: " + ", ".join(quickest) +
        f", {total_minutes} minutes"
    )

    dist_text = (
        "Shortest: " + ", ".join(shortest) +
        f", {total_km:.2f} km"
    )

    # Define stop-coloring rules for SVG
    def colors(stop):
        if stop in quickest and stop in shortest:
            return "darkcyan"      # both
        elif stop in quickest:
            return "orange"        # time shortest
        elif stop in shortest:
            return "green"         # distance shortest
        return "white"             # other stops

    # build dynamic file name from arguments, safely
    dep_safe = default_storage.get_valid_name(real_dep)
    dest_safe = default_storage.get_valid_name(real_dest)
    outfile_unique_name = f"shortest_path_{dep_safe}_{dest_safe}.svg"

    # generate colored SVG
    infile = os.path.join(settings.BASE_DIR, 'tram/templates/tram/images/gbg_tramnet.svg')
    outfile = os.path.join(settings.BASE_DIR, f'tram/templates/tram/images/generated/{outfile_unique_name}')

    # ensure output directory exists
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    
    # create colored SVG file
    color_svg_network(infile, outfile, colormap=colors)

    # return the path texts to be shown in the web page
    return time_text, dist_text, outfile

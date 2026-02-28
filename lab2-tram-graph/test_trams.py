import unittest
from trams import readTramNetwork
from graphs import dijkstra


class TestTrams(unittest.TestCase):

    def setUp(self):
        # Load the tram network once for all tests.
        self.G = readTramNetwork()

    def test_all_stops_exist_as_vertices(self):
        # All stops should appear in the graph's vertex set.
        stops = self.G.all_stops()
        verts = set(self.G.vertices())
        for s in stops:
            self.assertIn(s, verts, msg=f"{s} not in graph vertices")

    def test_lines_via_chalmers(self):
        # Lines via Chalmers should match Lab1 example.
        lines = self.G.lines_via_stop("Chalmers")
        # This is from Lab1 documentation: ['6', '7', '8', '10', '13']
        self.assertEqual(lines, ['6', '7', '8', '10', '13'])

    def test_shortest_path_stations_count(self):
        # When using the fewest stops as cost, the path from Chalmers to Järntorget should have at least two stops.
        paths = dijkstra(self.G, "Chalmers", cost=lambda u, v: 1)
        self.assertIn("Järntorget", paths)
        path = paths["Järntorget"]
        self.assertIsInstance(path, list)
        self.assertGreater(len(path), 1)

    def test_transition_times_non_negative(self):
        # All transition times on edges should be non-negative.
        positive_count = 0

        for a, b in self.G.edges():
            t = self.G.transition_time(a, b)
            self.assertIsNotNone(t, msg=f"no time for edge {a}-{b}")
            # Allow 0, but not negative
            self.assertGreaterEqual(t, 0, msg=f"negative time for edge {a}-{b}")
            if t > 0:
                positive_count += 1

        # There should be at least one edge with a strictly positive transition time.
        self.assertGreater(positive_count, 0, "no strictly positive transition times found")



if __name__ == '__main__':
    unittest.main()

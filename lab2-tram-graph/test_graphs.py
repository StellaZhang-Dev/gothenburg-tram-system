import unittest
from graphs import Graph, WeightedGraph, dijkstra

class TestGraphs(unittest.TestCase):

    def test_edges_vertices_consistent(self):
        # Every edge's endpoints must be in the vertex set.
        G = Graph([(1, 2), (2, 3)])
        for a, b in G.edges():
            self.assertIn(a, G.vertices())
            self.assertIn(b, G.vertices())

    def test_neighbors_symmetric(self):
        # If a is neighbor of b, then b is neighbor of a.
        G = Graph([(1, 2), (2, 3)])
        self.assertIn(2, list(G.neighbors(1)))
        self.assertIn(1, list(G.neighbors(2)))
        self.assertIn(3, list(G.neighbors(2)))
        self.assertIn(2, list(G.neighbors(3)))

    def test_weight_setting(self):
        # Weights should be stored and retrievable.
        WG = WeightedGraph([(1, 2)])
        WG.set_weight(1, 2, 7)
        self.assertEqual(WG.get_weight(1, 2), 7)

    def test_dijkstra_path(self):
        # Check if Dijkstra returns the correct shortest path.
        WG = WeightedGraph([(1, 2), (2, 3)])
        WG.set_weight(1, 2, 5)
        WG.set_weight(2, 3, 1)
        paths = dijkstra(WG, 1, cost=lambda u, v: WG.get_weight(u, v))
        self.assertEqual(paths[3], [1, 2, 3])

if __name__ == "__main__":
    unittest.main()

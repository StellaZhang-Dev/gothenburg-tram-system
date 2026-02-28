import networkx as nx
from graphviz import Graph as GVGraph

class Graph(nx.Graph):
    # Simple undirected graph based on networkx.Graph.
    def __init__(self, start=None):
        super().__init__(start)

    def vertices(self):
        # networkx uses nodes()
        return list(self.nodes())
    
    def edges(self):
        # Return all edges in the graph.
        return list(super().edges())

    def neighbors(self, v):
        # Return an iterator over neighbors of v.
        return super().neighbors(v)

    def __len__(self):
        # Number of vertices.
        return self.number_of_nodes()

    def add_vertex(self,a):
        # Add a vertex to the graph.
        self.add_node(a)

    def remove_vertex(self, v):
        # Remove a vertex and its incident edges.
        self.remove_node(v)

    def remove_edge(self, a, b):
        # Remove the edge between a and b.
        super().remove_edge(a, b)

    def get_vertex_value(self, v):
        # Returns None if no value is set.
        data = self.nodes[v]
        return data.get("value", None)

    def set_vertex_value(self, v, x):
        #If the vertex does not exist。
        if not self.has_node(v):
            self.add_node(v)
        self.nodes[v]["value"] = x


class WeightedGraph(Graph):
    # Graph where edges have a 'weight' attribute.
    def set_weight(self, a, b, w):
        # Set the weight on edge (a, b).
        if not self.has_edge(a, b):
            self.add_edge(a, b)
        self[a][b]["weight"] = w

    def get_weight(self, a, b):
        # Returns None if not set.
        if not self.has_edge(a, b):
            return None
        return self[a][b].get("weight", None)


# ---- helper for dijkstra ----

def costs2attributes(G, cost, attr="weight"):
    # Used to translate a cost function into edge attributes.
    for a, b in G.edges():
        G[a][b][attr] = cost(a, b)


def dijkstra(graph, source, cost=lambda u, v: 1):
    # Returns dict mapping target -> path .

    # Do not modify the original graph
    G = nx.Graph()
    G.add_nodes_from(graph.nodes(data=True))
    G.add_edges_from(graph.edges())
    
    costs2attributes(G, cost, attr="weight")

    # networkx shortest_path
    paths = nx.shortest_path(G, source=source, weight="weight")

    # Optionally sort
    return dict(sorted(paths.items(), key=lambda kv: kv[0]))


def visualize(graph, view="view", name="mygraph", nodecolors=None):
    # Visualize a graph with graphviz.
    dot = GVGraph(name)

    nodecolors = nodecolors or {}

    # Add nodes
    for v in graph.vertices():
        label = str(v)
        color = nodecolors.get(label, "black")
        dot.node(label, label=label, color=color)

    # Add edges
    for a, b in graph.edges():
        dot.edge(str(a), str(b))

    # Render
    if view == "view":
        dot.render(view=True)
    elif view == "pdf":
        dot.render()
    else:
        dot.render()

def view_shortest(G, source, target, cost=lambda u, v: 1):
    # Print and visualize the shortest path
    paths = dijkstra(G, source, cost)
    path = paths[target]
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)


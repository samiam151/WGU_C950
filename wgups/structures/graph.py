from wgups.structures import Node


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_node(self, new_node):
        self.adjacency_list[new_node] = []

    def add_directed_edge(self, from_node, to_node, weight=1.0):
        self.edge_weights[(from_node, to_node)] = weight
        self.adjacency_list[from_node].append(to_node)

    def add_undirected_edge(self, node_a, node_b, weight=1.0):
        self.add_directed_edge(node_a, node_b, weight)
        self.add_directed_edge(node_b, node_a, weight)

    def get_repr(self):
        s = "[Graph]:\n"
        s += ("-" * 10) + "\n"
        for i, node in enumerate(self.adjacency_list, start=1):
            s += f"{node.name}\n"
            for j, other_node in enumerate(self.adjacency_list, start=1):
                weight = self.edge_weights[(node, other_node)]
                if weight != "":
                    s += f"\t=> {other_node.name}: {weight}\n"
        return s

    def __str__(self):
        return self.get_repr()

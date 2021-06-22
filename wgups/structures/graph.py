from wgups.structures import Node
from typing import TypeVar, Generic

from wgups.structures.edge import Edge


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edges = {}

    def add_node(self, new_node):
        self.adjacency_list[new_node] = []

    def add_directed_edge(self, from_node, to_node, weight):
        if weight != '':
            edge = Edge(from_node, to_node, weight)
            self.edges[(from_node, to_node)] = edge
            if from_node not in self.adjacency_list:
                self.add_node(from_node)
            self.adjacency_list[from_node].append(to_node)

    def add_undirected_edge(self, node_a, node_b, weight):
        self.add_directed_edge(node_a, node_b, weight)
        self.add_directed_edge(node_b, node_a, weight)

    def lookup(self, node_a, node_b):
        return self.edges[(node_a, node_b)]

    def get_edges(self, node: Node):
        if node is None:
            return None
        else:
            edges = []
            nodes = self.adjacency_list[node]
            for end_node in nodes:
                _edge = self.edges[(node, end_node)]
                if _edge.weight == "0.0":
                    pass
                else:
                    edges.append(_edge)
            return edges

    def get_repr(self):
        s = "[Graph]:\n"
        s += ("-" * 10) + "\n"
        for i, start_node in enumerate(self.adjacency_list, start=1):
            # s += f"{node.name}\n"
            s += start_node.__str__() + "\n"
            for j, end_node in enumerate(self.adjacency_list, start=1):
                try:
                    edge = self.edges[(start_node, end_node)]
                    if edge is not None and edge.weight != "":
                        s += f"\t=> {end_node}: {edge}\n"
                except KeyError:
                    pass
        return s

    def __repr__(self):
        self.__str__()

    def __str__(self):
        return self.get_repr()

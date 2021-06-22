from .constants import *
from .packages import *

# from wgups.structures import Node
# from wgups.structures.edge import Edge
#
#
#
# def find_shortest_edge(node: Node, distance_map) -> Edge:
#     edges = distance_map.get_edges(node)
#     lowest = None
#
#     i = 0
#     for index, edge in enumerate(edges):
#         if edge.start_node == node:
#             i = index + 1
#             break
#
#     if len(edges) == 0:
#         return None
#
#     for edge in edges[i:]:
#         if lowest is not None:
#             if edge.weight != "0.0" and float(edge.weight) < float(lowest.weight):
#                 lowest = edge
#         else:
#             lowest = edge
#     return lowest
#
#
# def bfs(start_node: Node):
#     current_node = start_node
#     routes = [current_node]
#
#     while current_node is not None:
#         shortest_edge = find_shortest_edge(current_node)
#
#         if shortest_edge is not None:
#             current_node = shortest_edge.end_node
#         else:
#             current_node = None
#         routes.append(current_node)
#     return routes

from wgups.structures import Graph, Node


def get_distance(distance_graph: Graph, from_node: Node, to_node: Node):
    """
    Runtime: O(1)
    Space: O(1)
    """
    try:
        edge = distance_graph.edges[(from_node, to_node)]
        return float(edge.weight)
    except Exception:
        return None

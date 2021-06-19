import csv
from typing import List

from wgups.models import Post, Package
from wgups.structures import Graph, Node, HashSet


def load_packages() -> HashSet:
    package_hash_set: HashSet = HashSet()
    _path = "./wgups/data/data/packages.csv"

    try:
        with open(_path) as packageFile:
            for row in csv.reader(packageFile):
                package_hash_set.insert(Package(*row))
    except FileNotFoundError:
        print("File not found")

    return package_hash_set


def generate_nodes(rows: List[List[str]]) -> List[Node]:
    nodes = []
    current_node = None
    try:
        for i, row in enumerate(rows):
            current_node = row
            label = rows[i][0].split("\n")[0]
            node = Node(label)
            nodes.append(node)
    except KeyError:
        print(current_node)
    return nodes


def generate_posts(rows: List[List[str]]) -> List[Post]:
    posts: List[Post] = []
    current_post = None
    try:
        for i, row, in enumerate(rows):
            current_post = row
            label = rows[i][0].split("\n")[0]
            pieces = rows[i][1].split("\n")
            address_str = pieces[0].strip()
            zip_code = None if address_str == 'HUB' else pieces[1].strip(' ()')
            post = Post(label, address_str, zip_code)
            posts.append(post)
    except KeyError:
        print(current_post)
    return posts


def load_distances() -> Graph:
    distance_graph = Graph()
    _path = "./wgups/data/data/distances.csv"

    try:
        with open(_path) as packageFile:
            rows = []

            for row in csv.reader(packageFile):
                rows.append(row)

            distances = [row[2:] for row in rows[1:]]
            # nodes: List[Node] = generate_nodes(rows[1:])
            posts: List[Post] = generate_posts(rows[1:])
            return process_distances(posts, distance_graph, distances)

    except FileNotFoundError:
        print("File not found")

    return distance_graph


def process_distances(nodes: List[Node], distance_graph: Graph, distances: List[List[str]]) -> Graph:
    for i, node in enumerate(nodes):
        distance_graph.add_node(node)

        for j, d_node in enumerate(nodes):
            distance = distances[i][j] if distances[i][j] != "0" else ""
            distance_graph.add_directed_edge(node, d_node, distance)
    return distance_graph

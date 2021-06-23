import csv
from typing import List

import wgups.models as models
import wgups.structures as structures
from wgups.models import Post
from wgups.structures import Node


def load_packages() -> structures.HashSet[models.Package]:
    package_hash_set: structures.HashSet = structures.HashSet()
    _path = "./wgups/data/data/packages.csv"

    try:
        with open(_path) as packageFile:
            for row in csv.reader(packageFile):
                package_hash_set.insert(models.Package(*row))
    except FileNotFoundError:
        print("File not found")

    return package_hash_set


def generate_nodes(rows: List[List[str]], posts: List[models.Post]):
    nodes = []
    current_node = None
    try:
        for i, row in enumerate(rows):
            current_node = row
            name = rows[i][0].split("\n")[0]
            post = posts[i]
            node = structures.Node(name, post)
            nodes.append(node)
            post.node = node
    except KeyError:
        print(current_node)
    return nodes


def generate_posts(rows: List[List[str]]) -> List[models.Post]:
    posts: List[models.Post] = []
    current_post = None
    try:
        for i, row, in enumerate(rows):
            current_post = row
            label = rows[i][0].split("\n")[0]
            pieces = rows[i][1].split("\n")
            address_str = pieces[0].strip()
            zip_code = None if address_str == 'HUB' else pieces[1].strip(' ()')
            post = models.Post(label, address_str, zip_code)
            posts.append(post)
    except KeyError:
        print(current_post)
    return posts


def load_distances() -> (structures.Graph, List[Node], List[Post]):
    distance_graph = structures.Graph()
    _path = "./wgups/data/data/distances.csv"

    try:
        with open(_path) as packageFile:
            data_rows = []
            data_columns = []

            for row in csv.reader(packageFile):
                data_rows.append(row)

            for i in range(len(data_rows) + 1):
                column = []
                for row in data_rows:
                    column.append(row[i])
                data_columns.append(column)

            distances = [column[1:] for column in data_columns[2:]]
            posts: List[models.Post] = generate_posts(data_rows[1:])
            nodes: List[structures.Node] = generate_nodes(data_rows[1:], posts)

            for i in range(len(posts)):
                posts[i].node = nodes[i]

            return process_distances(nodes, distance_graph, distances), nodes, posts

    except FileNotFoundError:
        print("File not found")

    return distance_graph


def process_distances(nodes: List[structures.Node], distance_graph: structures.Graph, distances: List[List[str]]) -> structures.Graph:
    for i, node in enumerate(nodes):
        distance_graph.add_node(node)

        for j, d_node in enumerate(nodes):
            distance = distances[i][j] if distances[i][j] != "0" else ""
            distance_graph.add_undirected_edge(node, d_node, distance)
    return distance_graph

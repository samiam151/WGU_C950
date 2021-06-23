import sys
from typing import List

import wgups.models as models
from wgups.models.constraint import PackageConstraint, TruckConstraint
from wgups.structures import Clock, Node, Graph
import wgups.utils.distances as distance


class Truck:
    def __init__(self, _id, start_time="08:00", packages=None):
        if packages is None:
            packages = []
        self.id = _id
        self.packages = packages
        self.speed = 18
        self.package_limit = 16
        self.start_time: str = start_time
        self.miles_traveled = 0
        self.clock = Clock(self.start_time)
        self.current_node = None
        print(f"Truck {self.id} Start: {self.clock.get_time()}")

    def is_full(self):
        return len(self.packages) >= self.package_limit

    def has_package(self, p: models.Package):
        return p in self.packages

    def distance_to_time(self, d: float):
        return int((d / self.speed) * 60)

    """
    Determines if the given package can be delivered
    """
    def can_deliver(self, p: models.Package):
        # Accept any package with no constraints
        if not p.has_constraints():
            return True
        # Check constraints
        else:
            temp_can_deliver = True
            for c in p.constraints:
                if type(c) == TruckConstraint and self.id != int(c.required_truck):
                    temp_can_deliver = False

            return temp_can_deliver

    def deliver_package(self, graph: Graph, package: models.Package, nodes):
        destination_node = next((node for node in nodes if node.value.address == package.address), None)
        _distance_traveled = distance.get_distance(graph, self.current_node, destination_node)
        self.current_node = destination_node
        self.packages.remove(package)
        distance_traveled = _distance_traveled if _distance_traveled is not None else 0
        self.clock.add_minutes(self.distance_to_time(distance_traveled))
        print(f"Truck {self.id}: {self.clock.get_time()}, Distance: {distance_traveled}, "
              + f"Time: {self.distance_to_time(distance_traveled)}")

        return distance_traveled

    def deliver_packages(self, nodes: List[Node], distances: Graph, posts: List[models.Post]):
        self.current_node = nodes[0]
        distance_traveled: float = 0

        """
        Find out which package has the shortest distance (closest)
        """
        while self.packages:
            lowest_distance_package_index = None
            lowest_distance = sys.maxsize
            for index, destination_package in enumerate(self.packages):
                _distance = distance.get_distance(distances, self.current_node, destination_package.post.node)
                _distance = _distance if _distance is not None else 0
                if _distance < lowest_distance:
                    lowest_distance_package_index = index
                    lowest_distance = _distance

            distance_traveled += self.deliver_package(distances, self.packages[lowest_distance_package_index], nodes)

        print(f"Trip Miles: {distance_traveled}")
        return distance_traveled

    def add_package(self, p: models.Package):
        self.packages.append(p)

    def __repr__(self):
        s = f"[Truck] Id = {self.id}, Miles = {self.miles_traveled}, Start = {self.start_time} Package Count = {len(self.packages)}\n"
        for p in self.packages:
            s += f"\t => {p}\n"
        return s

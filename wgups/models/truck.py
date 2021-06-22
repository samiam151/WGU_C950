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

    def get_package_ids(self):
        return [package.id for package in self.packages]

    def is_full(self):
        return len(self.packages) >= self.package_limit

    def has_package(self, p: models.Package):
        return p in self.packages

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
        self.clock.add_minutes((distance_traveled / self.speed) * 60)
        print(f"Truck {self.id}: {self.clock.get_time()}")

        return distance_traveled

    def deliver_packages(self, nodes: List[Node], distances: Graph, posts: List[models.Post]):
        self.current_node = nodes[0]
        distance_traveled: float = 0

        def match_distance(p: models.Package):
            destination_node = next((node for node in nodes if node.value.address == p.address), None)
            d = distance.get_distance(distances, self.current_node, destination_node)
            return d

        """
        Find out which package has the shortest distance (closest)
        """
        # constrained_sorted_packages = sorted([p for p in self.packages if p.has_constraints()],
        #                                      key=lambda _p: match_distance(_p))
        # unconstrained_sorted_packages = sorted([p for p in self.packages if not p.has_constraints()],
        #                                        key=lambda _p: match_distance(_p))
        #
        # for package in constrained_sorted_packages:
        #     distance_traveled += self.deliver_package(distances, package, nodes)
        #
        # for package in unconstrained_sorted_packages:
        #     distance_traveled += self.deliver_package(distances, package, nodes)

        for package in self.packages:
            distance_traveled += self.deliver_package(distances, package, nodes)

        print("Trip Miles: ", distance_traveled)
        return distance_traveled

    def add_package(self, p: models.Package):
        self.packages.append(p)

    def add_packages(self, packages: List[models.Package]):
        for package in packages:
            self.add_package(package)

    def print_miles_traveled(self):
        print(f"[Truck:{self.id}] Miles Traveled: {self.miles_traveled}")

    def __repr__(self):
        s = f"[Truck] Id = {self.id}, Miles = {self.miles_traveled}, Start = {self.start_time} Package Count = {len(self.packages)}\n"
        for p in self.packages:
            s += f"\t => {p}\n"
        return s

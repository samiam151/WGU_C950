from typing import List

import wgups.models as models
from wgups.models.constraint import PackageConstraint, TruckConstraint
from wgups.structures import Clock, Node, Graph


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
            for c in p.constraints:
                if type(c) == TruckConstraint and self.id != int(c.required_truck):
                    return False

    def deliver_packages(self, nodes: List[Node], distances: Graph, posts: List[models.Post]):
        self.current_node = nodes[0]

        def match_address(y: models.Post):
            return y.address == self.current_node.address

        """
        Find out which package has the shortest distance (closest)
        """
        for package in self.packages:
            addresses = [p.address for p in self.packages]


            # node = next((post.node for post in posts if match_address(post)), None)

            # distances.get_edges()
            # self.packages.remove(package)

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

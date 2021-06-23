import sys
from typing import List

import wgups.models as models
from wgups.models.constraint import PackageConstraint, TruckConstraint
from wgups.structures import Timer, Node, Graph
import wgups.utils.distances as distance
from wgups.utils import PackageStatus


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
        self.clock = Timer(self.start_time)
        self.location = None
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

    def deliver_package(self, graph: Graph, package: models.Package, package_distance: float):
        destination_node = package.post.node
        self.location = destination_node
        package.status = PackageStatus.delivered()
        self.packages.remove(package)
        self.clock.add_minutes(self.distance_to_time(package_distance))

        print(f"Truck {self.id}: {self.clock.get_time().time()}, Distance: {package_distance}, "
              + f"Time: {self.distance_to_time(package_distance)}")
        print(f"\t{package}")

        return package_distance

    def find_shortest_node(self):
        pass

    def deliver_packages(self, nodes: List[Node], distances: Graph, posts: List[models.Post]):
        self.location = nodes[0]
        distance_traveled: float = 0
        packages_delivered = 0

        distance_memo = {}
        while len(self.packages) > 0:
            lowest_distance_package_index = None
            lowest_distance: float = sys.maxsize
            for index, destination_package in enumerate(self.packages):
                destination_node = destination_package.post.node
                current_trip = (self.location, destination_node)
                calculated_distance = None

                if current_trip in distance_memo:
                    calculated_distance = distance_memo[current_trip]
                else:
                    calculated_distance = distance.get_distance(distances, self.location, destination_node)
                    distance_memo[current_trip] = calculated_distance

                calculated_distance = calculated_distance if calculated_distance is not None else 0
                if calculated_distance < lowest_distance:
                    lowest_distance_package_index = index
                    lowest_distance = calculated_distance

            distance_traveled += self.deliver_package(distances, self.packages[lowest_distance_package_index],
                                                      lowest_distance)
            packages_delivered += 1

        print("=====================================================")
        print(f"Trip Miles: {distance_traveled}, Packages Delivered: {packages_delivered}")
        print("=====================================================")
        return distance_traveled

    def add_package(self, p: models.Package):
        self.packages.append(p)

    def __repr__(self):
        s = f"[Truck] Id = {self.id}, Miles = {self.miles_traveled}, Start = {self.start_time} Package Count = {len(self.packages)}\n"
        for p in self.packages:
            s += f"\t => {p}\n"
        return s

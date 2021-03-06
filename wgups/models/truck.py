import sys
from typing import List, Union

import wgups.models as models
from wgups.models.constraint import TruckConstraint, TimeConstraint
from wgups.models.report import Report
from wgups.structures import Timer, Node, Graph
import wgups.utils.distances as distance
from wgups.utils import PackageStatus


class Truck:
    def __init__(self, _id, start_time="08:00:00", packages=None):
        if packages is None:
            packages = []
        self.id = _id
        self.packages = packages
        self.speed = 18
        self.package_limit = 16
        self.start_time: str = start_time
        self.miles_traveled = 0
        self.clock = Timer(self.start_time)
        self.location: Union[Node, None] = None
        self.current_trip_record = []

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
        """
        Runtime: O(n)
        Space: O(n)
        """
        # Accept any package with no constraints
        if not p.has_constraints():
            return True
        # Check constraints
        else:
            temp_can_deliver = True
            for c in p.constraints:
                # Handle required truck constraint
                if type(c) == TruckConstraint and self.id != int(c.required_truck):
                    temp_can_deliver = False

                # Handle time constraints
                if type(c) == TimeConstraint:
                    # Make sure package is available before the truck's start time
                    if c.arrival_time is not None:
                        truck_start_time = self.clock.get_time().time()
                        package_arrival_time = c.arrival_time.time()
                        if package_arrival_time > truck_start_time:
                            temp_can_deliver = False

            return temp_can_deliver

    def return_home(self, distances, node):
        current_location = self.location
        calculated_distance = distance.get_distance(distances, self.location, node)
        self.clock.add_minutes(self.distance_to_time(calculated_distance))
        self.location = node

        return calculated_distance

    def deliver_package(self, package: models.Package, package_distance: float):
        """
        Runtime: O(n)
        Space: O(n)
        """
        destination_node = package.post.node
        self.location = destination_node
        package.status = PackageStatus.delivered()
        for p in self.packages:
            if p.id == package.id:
                self.packages.remove(package)
        self.clock.add_minutes(self.distance_to_time(package_distance))
        package.delivered_at = self.clock.get_time()

        return package_distance

    def find_shortest_node(self, given_packages, distances, distance_memo):
        lowest_distance_package_index = None
        lowest_distance: float = sys.maxsize
        for index, destination_package in enumerate(given_packages):
            destination_node = destination_package.post.node
            current_trip = (self.location, destination_node)

            if current_trip in distance_memo:
                calculated_distance = distance_memo[current_trip]
            else:
                calculated_distance = distance.get_distance(distances, self.location, destination_node)
                distance_memo[current_trip] = calculated_distance

            calculated_distance = calculated_distance if calculated_distance is not None else 0
            if calculated_distance < lowest_distance:
                lowest_distance_package_index = index
                lowest_distance = calculated_distance

        return lowest_distance_package_index, lowest_distance

    def deliver_packages(self, nodes: List[Node], reports: List[Report], distances: Graph):
        self.current_trip_record = []
        self.location = nodes[0]
        distance_traveled: float = 0

        for p in self.packages:
            p.status = PackageStatus.en_route()
            p.loaded_at = self.clock.get_time()

        deadline_packages = [p for p in self.packages if p.has_constraint(TimeConstraint)]
        non_deadline_packages = [p for p in self.packages if p not in deadline_packages]

        distance_memo = {}
        for package_list in [deadline_packages, non_deadline_packages]:
            while len(package_list) > 0:
                lowest_distance_package_index, lowest_distance = \
                    self.find_shortest_node(package_list, distances, distance_memo)
                next_package = package_list[lowest_distance_package_index]

                distance_traveled += self.deliver_package(next_package,
                                                          lowest_distance)
                reports.append(Report(
                    package=next_package,
                    time=self.clock.get_time()
                ))
                package_list.remove(next_package)

        distance_traveled += self.return_home(distances, nodes[0])
        return distance_traveled

    def add_package(self, p: models.Package):
        self.packages.append(p)

    def __repr__(self):
        s = f"[Truck] Id = {self.id}, Miles = {self.miles_traveled}, Start = {self.start_time} \n"
        for p in self.packages:
            s += f"\t => {p}\n"
        return s

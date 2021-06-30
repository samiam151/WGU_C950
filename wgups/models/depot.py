from itertools import cycle
from typing import List

import wgups.models as models
from wgups.models.constraint import PackageConstraint
from wgups.structures import HashSet, Graph, Node


class Depot:
    def __init__(self, distance_map: Graph, packages: HashSet):
        self.trucks = [models.Truck(1), models.Truck(2, start_time="10:30:00")]
        self.packages = packages.all()
        self.distances = distance_map
        self.total_miles_traveled: float = 0
        self.package_reports = []

    def deliver_packages(self, nodes: List[Node], posts: List[models.Post]):
        unconstrained_packages = []
        constrained_packages = []
        package_constrained_packages = []

        for package in self.packages:
            if package.has_constraints():
                has_package_constraint = False
                for constraint in package.constraints:
                    if type(constraint) == PackageConstraint:
                        has_package_constraint = True

                if has_package_constraint:
                    package_constrained_packages.append(package)
                else:
                    constrained_packages.append(package)
            else:
                unconstrained_packages.append(package)

        truck_index = cycle(list(range(len(self.trucks))))
        while len(package_constrained_packages + unconstrained_packages + constrained_packages):
            truck: models.Truck = self.trucks[next(truck_index)]

            deliverable_constrained_packages = [
                p for p in constrained_packages if truck.can_deliver(p) and p not in package_constrained_packages]

            deliverable_regular_packages = [
                p for p in unconstrained_packages if truck.can_deliver(p)]

            for i in range(len(package_constrained_packages)):
                package = package_constrained_packages[0]
                if not truck.is_full() and not truck.has_package(package):
                    truck.add_package(package)
                    package_constrained_packages.remove(package)

            for package in deliverable_constrained_packages:
                if not truck.is_full() and not truck.has_package(package):
                    truck.add_package(package)
                    constrained_packages.remove(package)

            for package in deliverable_regular_packages:
                if not truck.is_full() and not truck.has_package(package):
                    truck.add_package(package)
                    unconstrained_packages.remove(package)

            self.total_miles_traveled += truck.deliver_packages(nodes, self.package_reports, self.distances)

        # print("Total Miles Traveled:", "{:.2f}".format(self.total_miles_traveled))

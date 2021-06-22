from itertools import cycle
from typing import List, TypeVar

import wgups.models as models
from wgups.structures import HashSet, Graph, Node

class Depot:
    def __init__(self, distance_map: Graph, packages: HashSet):
        self.trucks = [models.Truck(1, start_time="09:30"), models.Truck(2)]
        self.packages = packages.all()
        self.distances = distance_map

    def deliver_packages(self, nodes: List[Node], posts: List[models.Post]):
        unconstrained_packages = []
        constrained_packages = []

        assigned_map = {}

        for i in range(len(self.trucks)):
            assigned_map[i + 1] = []

        for package in self.packages:
            if package.has_constraints():
                constrained_packages.append(package)
            else:
                unconstrained_packages.append(package)

        truck_index = cycle(list(range(len(self.trucks))))
        delivered = 0

        while delivered < len(self.packages):
            truck: models.Truck = self.trucks[next(truck_index)]
            deliverable_constrained_packages = [
                p for p in constrained_packages if truck.can_deliver(p)]

            deliverable_regular_packages = [
                p for p in unconstrained_packages if truck.can_deliver(p)]

            for package in deliverable_constrained_packages:
                if not truck.is_full() and not truck.has_package(package):
                    truck.add_package(package)
                    constrained_packages.remove(package)
                    delivered += 1

            for package in deliverable_regular_packages:
                if not truck.is_full() and not truck.has_package(package):
                    truck.add_package(package)
                    unconstrained_packages.remove(package)
                    delivered += 1

            truck.deliver_packages(nodes, self.distances, posts)

            break

        return

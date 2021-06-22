from typing import List

import wgups.models as models
import wgups.models.constraint as constraint
import wgups.structures as structures
from itertools import cycle
from wgups.utils import PackageStatus

constraint_cues = {
    "co_package": "Must be delivered with ",
    "delay": "Delayed on flight---will not arrive to depot until ",
    "truck": "Can only be on truck ",
    "wrong_address": "Wrong address listed"
}


def add_package_constraints(packages: structures.HashSet) -> structures.HashSet:
    for ac_package in sorted(packages.all(), key=lambda x: x.id):
        # Add address constraints
        if constraint_cues.get("wrong_address") in ac_package.notes:
            # ac_package.constraints.append(constraint.AddressConstraint())
            ac_package.address = "410 S State St"
            ac_package.city = "Salt Lake City"
            ac_package.state = "84111"
            ac_package.zip = "UT"
            ac_package.constraints.append(constraint.TimeConstraint(arrival_time="1020"))

        # Add co-package constraints
        if constraint_cues.get("co_package") in ac_package.notes:
            p_ids = ac_package.notes.split(constraint_cues.get("co_package"))[1]
            ac_package.constraints.append(constraint.PackageConstraint(p_ids.split(", ")))

        # Add deadline constraints
        if ac_package.deadline != 'EOD':
            ac_package.constraints.append(constraint.TimeConstraint(deadline=ac_package.deadline))

        # Add delay constraints
        if constraint_cues.get("delay") in ac_package.notes:
            arrival_time = ac_package.notes.split(constraint_cues.get("delay"))[1]
            ac_package.constraints.append(constraint.TimeConstraint(arrival_time=arrival_time))

        # Add trick requirement constraints
        if constraint_cues.get("truck") in ac_package.notes:
            required_truck = ac_package.notes.split(constraint_cues.get("truck"))[1]
            ac_package.constraints.append(constraint.TruckConstraint(required_truck))

    return packages


def distribute_packages(packages: structures.HashSet, dp_depot):
    ps: List[models.Package] = packages.all()
    unconstrained_packages = []
    constrained_packages = []
    assigned_map = {}

    for i in range(len(dp_depot.trucks)):
        assigned_map[i + 1] = []

    for pp in ps:
        if pp.has_constraints():
            constrained_packages.append(pp)
        else:
            unconstrained_packages.append(pp)

    def assign_package(assigning_truck: models.Truck, ap_package: models.Package) -> bool:
        if not assigning_truck.is_full() and not assigning_truck.has_package(ap_package):
            assigning_truck.packages.append(ap_package)
            chosen_list = constrained_packages if ap_package.has_constraints() else unconstrained_packages
            chosen_list.remove(ap_package)
            assigned_map[assigning_truck.id].append(ap_package.id)
            ap_package.status = PackageStatus.assigned()
            return True
        return False

    print("Unconstrained at Start:", len(unconstrained_packages))
    print("Constrained at Start:", len(constrained_packages))

    truck_index = cycle(list(range(len(dp_depot.trucks))))
    package_index = 0

    while len(constrained_packages) > 0:
        c_package = constrained_packages[0]
        for dp_constraint in c_package.constraints:
            if isinstance(dp_constraint, constraint.TruckConstraint):
                print(f"Package ID: {c_package.id}, {dp_constraint}")
                # required_truck: models.Truck = dp_depot.trucks[int(dp_constraint.required_truck) - 1]
                # assign_package(required_truck, c_package)
                # break

            if isinstance(dp_constraint, constraint.TimeConstraint):
                print(f"Package ID: {c_package.id}, {dp_constraint}")
                # if dp_constraint.deadline is not None:
                #     t = dp_depot.trucks[next(truck_index)]
                #     assign_package(t, c_package)
                #     break

            if isinstance(dp_constraint, constraint.PackageConstraint):
                print(f"Package ID: {c_package.id}, {dp_constraint}")
                # co_packages = dp_constraint.co_packages
                # for dp_truck in dp_depot.trucks:
                #     if c_package.id in assigned_map[dp_truck.id]:
                #         assign_package(dp_truck.id, c_package)
                #         break

        constrained_packages = constrained_packages[1:]

    print("Unconstrained after Constraints:", len(unconstrained_packages))
    print("Constrained after Constraints:", len(constrained_packages))

    while len(unconstrained_packages) > 0:
        u_package = unconstrained_packages[package_index]
        for i in range(len(dp_depot.trucks)):
            next_index = next(truck_index)
            if assign_package(dp_depot.trucks[next_index], u_package):
                break

    print("Unconstrained at End:", len(unconstrained_packages))
    print("Constrained at End:", len(constrained_packages))

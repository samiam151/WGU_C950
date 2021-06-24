from typing import List
from datetime import datetime

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
            today = datetime.today()
            d = datetime(today.year, today.month, today.day, 10, 20)
            ac_package.constraints.append(constraint.TimeConstraint(arrival_time=d))

        # Add co-package constraints
        if constraint_cues.get("co_package") in ac_package.notes:
            p_ids = ac_package.notes.split(constraint_cues.get("co_package"))[1]
            split_pids = p_ids.split(", ")
            ac_package.constraints.append(constraint.PackageConstraint(p_ids.split(", ")))

            other_packages = [p for p in packages.all() if str(p.id) in split_pids]
            for other_package in other_packages:
                other_package.constraints.append(constraint.PackageConstraint())

        # Add deadline constraints
        if ac_package.deadline != 'EOD':
            ac_package.constraints.append(constraint.TimeConstraint(deadline=ac_package.deadline))

        # Add delay constraints
        if constraint_cues.get("delay") in ac_package.notes:
            arrival_time = ac_package.notes.split(constraint_cues.get("delay"))[1]
            arrival_times = [int(n) for n in arrival_time.split(" ")[0].split(":")]
            today = datetime.today()
            d = datetime(today.year, today.month, today.day, int(arrival_times[0]), int(arrival_times[1]))
            ac_package.constraints.append(constraint.TimeConstraint(arrival_time=d))

        # Add trick requirement constraints
        if constraint_cues.get("truck") in ac_package.notes:
            required_truck = ac_package.notes.split(constraint_cues.get("truck"))[1]
            ac_package.constraints.append(constraint.TruckConstraint(required_truck))

    return packages

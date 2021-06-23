from wgups.utils.constants import ConstraintType


class Constraint:
    def __init__(self):
        self.type = None

    def __str__(self):
        s = f"[[Constraint] {self.type}] "
        _vars = vars(self)
        for k in _vars.keys():
            s += f"{k.upper()} = {_vars[k]}, "
        return s


class TruckConstraint(Constraint):
    def __init__(self, truck=None):
        Constraint.__init__(self)
        self.type = ConstraintType.truck()
        self.required_truck = truck


class TimeConstraint(Constraint):
    def __init__(self, arrival_time=None, deadline=None):
        Constraint.__init__(self)
        self.type = ConstraintType.time()
        self.arrival_time = arrival_time
        self.deadline = deadline


class PackageConstraint(Constraint):
    def __init__(self, co_packages=None):
        Constraint.__init__(self)
        if co_packages is None:
            co_packages = []
        self.type = ConstraintType.co_package()
        self.co_packages = co_packages

from typing import Type

from wgups.utils.constants import PackageStatus


class Package:
    def __init__(self, _id, address, city, state, _zip, deadline, weight, notes):
        self.id: int = int(_id)
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip: int = int(_zip)
        self.deadline: str = deadline
        self.weight: int = int(weight)
        self.notes: str = notes
        self.constraints = []
        self.status = PackageStatus.unassigned()
        self.node = None
        self.post = None

    def has_constraints(self):
        return len(self.constraints) > 0

    def has_constraint(self, constraint_type: Type):
        has_constraint_type = False
        for c in self.constraints:
            if type(c) == constraint_type:
                has_constraint_type = True
        return has_constraint_type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        constraints = [c.type for c in self.constraints]
        return f"[Package]: Id = {self.id}, Status: {self.status}, Address = {str(self.address)}, Constraints = {constraints}"


from typing import Type, Union

from wgups.structures import Timer
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
        self.status = PackageStatus.at_hub()
        self.node = None
        self.post = None
        self.loaded_at: Union[Timer, None] = None
        self.delivered_at: Union[Timer, None] = None

    def has_constraints(self):
        """
        Runtime: O(1)
        Space: O(1)
        """
        return len(self.constraints) > 0

    def has_constraint(self, constraint_type: Type):
        """
        Runtime: O(n)
        Space: O(n)
        """
        has_constraint_type = False
        for c in self.constraints:
            if type(c) == constraint_type:
                has_constraint_type = True
        return has_constraint_type

    def mark_status_en_route(self):
        """
        Runtime: O(1)
        Space: O(1)
        """
        self.status = PackageStatus.en_route()

    def mark_status_delivered(self):
        """
        Runtime: O(1)
        Space: O(1)
        """
        self.status = PackageStatus.delivered()

    def get_status_at(self, time: Timer = None):
        """
        Runtime: O(1)
        Space: O(1)
        """
        if time is None:
            return self.get_status_at(Timer.create_time(17))
        if self.delivered_at is not None and self.delivered_at < time:
            return PackageStatus.delivered()
        if self.loaded_at is not None and self.loaded_at < time:
            return PackageStatus.en_route()
        return PackageStatus.at_hub()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        constraints = [c.type for c in self.constraints]
        return f"[Package]: Id = {self.id}, Status: {self.status}, Address = {str(self.address)}, Constraints = {constraints} "

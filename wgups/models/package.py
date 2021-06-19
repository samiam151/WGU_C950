import string


class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, notes):
        self.id: int = int(id)
        self.address: string = address
        self.city: string = city
        self.state: string = state
        self.zip: int = int(zip)
        self.deadline: string = deadline
        self.weight: int = int(weight)
        self.notes: string = notes

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"[Package]: {self.id}"

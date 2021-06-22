class Node:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # return f"[Node]: {self.name}\n\t\t[Value]: {self.value}"
        return f"[Node]: {self.name}"

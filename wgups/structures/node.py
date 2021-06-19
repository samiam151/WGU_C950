class Node:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"[Node]: {self.label}"

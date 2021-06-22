class Edge:
    def __init__(self, start, end, weight):
        self.weight = weight if weight != "" else 0.0
        self.start_node = start
        self.end_node = end
        self.is_self_route = self.start_node == self.end_node

    def __str__(self):
        return f"[Edge]: Weight = {self.weight} Start = {self.start_node} | End = {self.end_node}"

    def __repr__(self):
        return self.__str__()

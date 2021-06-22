import string

from wgups.structures import Node


class Post:
    def __init__(self, name: string, address: string, zip_code: string, node: Node=None) -> None:
        self.name = name
        self.address = address
        self.zip_code = zip_code
        self.node = node

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        s = f"[Post] {self.name} / {self.address}"
        # s += ("-" * 10 + "\n")
        # s += f"Name: {self.name}\n"
        # s += f"Address: {self.address}\n"
        # s += f"Zip Code: {self.zip_code}"
        return s

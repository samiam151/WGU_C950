import string


class Post:
    def __init__(self, name: string, address: string, zip_code: string) -> None:
        self.name = name
        self.address = address
        self.zip_code = zip_code

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        s = f"[Post] {self.name}"
        # s += ("-" * 10 + "\n")
        # s += f"Name: {self.name}\n"
        # s += f"Address: {self.address}\n"
        # s += f"Zip Code: {self.zip_code}"
        return s

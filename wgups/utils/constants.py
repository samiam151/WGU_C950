class PackageStatus:
    @staticmethod
    def at_hub():
        return "At the Hub"

    @staticmethod
    def en_route():
        return "En Route"

    @staticmethod
    def delivered():
        return "Delivered"


class ConstraintType:
    @staticmethod
    def address():
        return "Address"

    @staticmethod
    def co_package():
        return "Package"

    @staticmethod
    def time():
        return "Time"

    @staticmethod
    def truck():
        return "Truck"

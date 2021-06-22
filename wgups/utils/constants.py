class PackageStatus:
    @staticmethod
    def unassigned():
        return "Un-Assigned"

    @staticmethod
    def assigned():
        return "Assigned"


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

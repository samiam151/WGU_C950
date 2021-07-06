from datetime import datetime

from wgups.models import Package


class Report:
    def __init__(self, package: Package, time: datetime):
        self.time = time
        self.package = package

    def __repr__(self):
        return f"[Report] Package={self.package.id} Time={self.time.time()}\n"

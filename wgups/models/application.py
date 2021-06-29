from typing import List

from wgups.data.loader import load_packages, load_distances
from wgups.models import Depot, Package, Post, Report
from wgups.structures import HashSet, Graph, Timer
from wgups.utils import add_package_constraints


class Application:
    def __init__(self):
        self.distance_graph, self.nodes, self.posts = load_distances()
        self.packages: HashSet[Package] = load_packages()
        self.depot: Depot = Depot(self.distance_graph, self.packages)

    def initialize(self):
        for index, package in enumerate(self.packages.all()):
            package.post = next((post for post in self.posts if package.address == post.address), None)

        self.packages = add_package_constraints(self.packages)
        self.depot.deliver_packages(self.nodes, self.posts)

    def get_reports(self):
        return self.depot.package_reports

    def run_time_reports(self):
        minutes = None
        seconds = None
        given_time = input("Enter time, hh:mm:ss format, seconds optional")
        if len(given_time) == 0:
            minutes, seconds = 12, 30
        else:
            given_time_split = given_time.split(":")
            minutes, seconds = int(given_time_split[0]), int(given_time_split[1])

        time = Timer.create_time(minutes, seconds)
        last_report: Report = None
        for index, report in enumerate(self.get_reports()):
            if report.time > time:
                last_report = self.get_reports()[index - 1]
                break

        print(last_report)

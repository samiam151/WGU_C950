import re
import time
from typing import List

from wgups.data.loader import load_packages, load_distances
from wgups.models import Depot, Package, Post, Report
from wgups.structures import HashSet, Graph, Timer
from wgups.utils import add_package_constraints


def get_user_time():
    time_regex = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    hours = None
    minutes = None
    print("Enter time in HH:MM format:")
    given_time = input("> ")

    if time_regex.match(given_time):
        given_time_split = given_time.split(":")
        hours, minutes = int(given_time_split[0]), int(given_time_split[1])
        return Timer.create_time(hours, minutes)

    print("Please enter time in the format HH:MM")
    return None


def get_user_package_id():
    print("Enter the requested Package ID:")
    return int(input("> "))


class Application:
    def __init__(self):
        self.distance_graph, self.nodes, self.posts = load_distances()
        self.packages: HashSet[Package] = load_packages()
        self.depot: Depot = Depot(self.distance_graph, self.packages)

        self.commands = {
            "all": {
              "method": self.print_all_package_status_at_time,
              "description": "Displays the status of all packages at a chosen times"
            },
            "package": {
                "method": self.print_package_status_at_time,
                "description": "Displays the status of a chosen package at a chosen time"
            },
            "total-mileage": {
                "method": self.print_total_mileage,
                "description": "Displays the total mileage across all trucks"
            }
        }
        self.exit_commands = ['quit', 'exit']

    def initialize(self):
        for index, package in enumerate(self.packages.all()):
            package.post = next((post for post in self.posts if package.address == post.address), None)

        self.packages = add_package_constraints(self.packages)
        self.depot.deliver_packages(self.nodes, self.posts)

    def display_options(self):
        print("Please choose an option below:")
        for index, command in enumerate(self.commands.keys()):
            print(f"\t{index + 1}. {command} - {self.commands.get(command).get('description')}")
        print(f"Enter 'quit', or 'exit' to exit the application")

    def print_total_mileage(self):
        print("Total Miles Traveled:", "{:.2f}".format(self.depot.total_miles_traveled))

    def get_reports(self):
        return self.depot.package_reports

    def print_all_package_status_at_time(self):
        user_time = get_user_time()

        if user_time is not None:
            for package in self.depot.packages:
                status = package.get_status_at(user_time)
                print(f"Package Id: {package.id}, Status: {status}")

    def print_package_status_at_time(self):
        user_time = get_user_time()
        package_id = get_user_package_id()

        if user_time is not None and package_id is not None:
            package: Package = next((report.package for report in self.get_reports()
                                     if report.package.id == package_id), None)
            status = package.get_status_at(user_time)
            print(f"Package: {package.id}, Status: {status}, Time: {user_time.time()}")

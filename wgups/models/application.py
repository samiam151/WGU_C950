import re
from tabulate import tabulate

from wgups.data.loader import load_packages, load_distances
from wgups.models import Depot, Package
from wgups.models.constraint import TimeConstraint
from wgups.structures import HashSet, Timer
from wgups.utils import add_package_constraints


def get_user_time():
    """
    Accepts a time from the user, test to make sure that the
    time is in the correct format
    """
    time_regex = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    print("Enter time in HH:MM format:")
    given_time = input("> ")

    if time_regex.match(given_time):
        given_time_split = given_time.split(":")
        hours, minutes = int(given_time_split[0]), int(given_time_split[1])
        return Timer.create_time(hours, minutes)

    print("Please enter time in the format HH:MM")
    return None


def get_user_package_id():
    """
     Accepts the package ID from the user
    """
    print("Enter the requested Package ID:")
    return int(input("> "))


class Application:
    """
    Controls the flow of the application
    """
    def __init__(self):
        self.distance_graph, self.nodes, self.posts = load_distances()
        self.packages: HashSet[Package] = load_packages()
        self.depot: Depot = Depot(self.distance_graph, self.packages)

        """
        A dictionary of prompts to present to the user
        """
        self.input_prompts = {
            "enter_command": 'Please enter a command:\n> ',
            "incorrect_command": "Please enter a valid command from the options below"
        }
        """
        A dictionary of commands the user can enter to run
        """
        self.commands = {
            "all": {
              "method": self.print_table_packages,
              "description": "Displays the status of all packages at a chosen times"
            },
            "package": {
                "method": self.print_package_status_at_time,
                "description": "Displays the status of a chosen package at a chosen time"
            },
            "miles": {
                "method": self.print_total_mileage,
                "description": "Displays the total mileage across all trucks"
            }
        }
        self.exit_commands = ['quit', 'exit']

    def initialize(self):
        for index, package in enumerate(self.packages.all()):
            package.post = next((post for post in self.posts if package.address == post.address), None)

        self.packages = add_package_constraints(self.packages)
        self.depot.deliver_packages(self.nodes)

    def display_options(self):
        print("Please choose an option below:")
        for index, command in enumerate(self.commands.keys()):
            print(f"\t{index + 1}. {command} - {self.commands.get(command).get('description')}")
        print(f"Enter 'quit', or 'exit' to exit the application")

    def print_total_mileage(self):
        print("Total Miles Traveled:", "{:.2f}".format(self.depot.total_miles_traveled))

    def get_reports(self):
        return self.depot.package_reports

    def print_package_status_at_time(self):
        user_time = get_user_time()
        package_id = get_user_package_id()

        if user_time is not None and package_id is not None:
            package: Package = next((report.package for report in self.get_reports()
                                     if report.package.id == package_id), None)
            status = package.get_status_at(user_time)
            print(f"Package: {package.id}, Status: {status}, Time: {user_time.time()}")

    def print_table_packages(self):
        def get_deadline(pp: Package):
            if pp.has_constraint(TimeConstraint):
                cs = next((c for c in pp.constraints if type(c) == TimeConstraint and c.deadline is not None), None)
                if cs is not None:
                    return cs.deadline
                return "EOD"
            else:
                return "EOD"

        user_time = get_user_time()
        package_data = []
        table_headers = ["Id", "Address", "Deadline", "City", "Zip Code", "Weight", "Status"]

        for p in self.depot.packages:
            package_data.append([
                p.id,
                p.address,
                get_deadline(p),
                p.city,
                p.zip,
                p.weight,
                p.get_status_at(user_time)
            ])
        print(tabulate(package_data, headers=table_headers))

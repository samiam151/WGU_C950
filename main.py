from wgups.data.loader import load_packages, load_distances
from wgups.models import Depot, Package
from wgups.structures import HashSet
from wgups.utils import add_package_constraints, distribute_packages

if __name__ == '__main__':
    packages: HashSet[Package] = load_packages()
    distance_graph, nodes, posts = load_distances()

    for package in packages.all():
        package.post = next((post for post in posts if post.address == package.address), None)

    depot = Depot(distance_graph, packages)

    packages = add_package_constraints(packages)

    depot.deliver_packages(nodes, posts)
    # [print(t) for t in depot.trucks]


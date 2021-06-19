import wgups.data.loader as loader

if __name__ == '__main__':
    packages = loader.load_packages()
    distance_map = loader.load_distances()

    # print(packages)
    print(distance_map)


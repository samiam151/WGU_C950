from typing import List, TypeVar, Generic

T = TypeVar('T')


class HashSet(Generic[T]):
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, item):
        """
        Runtime: O(1)
        Space: O(1)
        """
        # get the bucket list where this item will go.
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        bucket_list.append(item)

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def lookup(self, key):
        """
        Runtime: O(1)
        Space: O(1)
        """
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        if key in bucket_list:
            # find the item's index and return the item that is in the bucket list.
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            # the key is not found.
            return None

    def all(self) -> List[T]:
        """
        Runtime: O(n)
        Space: O(n)
        """
        items: List[T] = []
        for bucket in self.table:
            for v in bucket:
                items.append(v)
        return sorted(items, key=lambda x: x.id)

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        """
        Runtime: O(1)
        Space: O(1)
        """
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)

    def __repr__(self) -> str:
        value = f"[HashTable]:\n{'-' * 10}\n"
        i = 1
        for bucket in self.table:
            value += f"bucket {i} =>\n"
            for v in bucket:
                value += f"\t{v}\n"
            i += 1
        return value

    def __str__(self) -> str:
        return self.__repr__()

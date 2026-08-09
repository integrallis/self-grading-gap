class RecentlyUsedItemsList:
    def __init__(self, capacity=5):
        self.capacity_limit = capacity
        self.items = []

    def add(self, item):
        if item is None:
            raise Exception("List items should not be Empty or Null. But it was [None]")
        if item == "":
            raise Exception("List items should not be Empty or Null. But it was []")
        if item not in self.items:
            self.items.insert(0, item)
            if len(self.items) > self.capacity_limit:
                self.items.pop()

    def count(self):
        return len(self.items)

    def get_all(self):
        return self.items[:]

    def capacity(self):
        return self.capacity_limit

    def get(self, index):
        if index < 0:
            raise Exception(f"supplied index [{index}] should be non-negative and not greater than [{len(self.items) - 1}].")
        if index >= len(self.items):
            raise Exception(f"supplied index [{index}] should not greater than [{len(self.items) - 1}].")
        return self.items[index]
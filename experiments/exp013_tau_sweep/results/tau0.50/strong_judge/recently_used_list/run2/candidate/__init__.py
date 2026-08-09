class RecentlyUsedItemsList:
    def __init__(self, capacity=5):
        self._capacity = capacity
        self.items = []

    def add(self, item):
        if item is None or item == "":
            raise Exception(f"List items should not be Empty or Null. But it was [{item}]")
        if item in self.items:
            self.items.remove(item)
        elif len(self.items) >= self._capacity:
            self.items.pop()  # Remove the oldest item
        self.items.insert(0, item)  # Add to the front

    def count(self):
        return len(self.items)

    def read(self):
        return self.items.copy()

    def get(self, index):
        if index < 0:
            raise Exception(f"supplied index [{index}] should be non-negative and not greater than [{len(self.items) - 1}].")
        if index >= len(self.items):
            raise Exception(f"supplied index [{index}] should not greater than [{len(self.items) - 1}].")
        return self.items[index]

    def capacity(self):
        return self._capacity
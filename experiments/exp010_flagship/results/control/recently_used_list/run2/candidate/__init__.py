class RecentlyUsedItemsList:
    def __init__(self, capacity=10):
        self.capacity_value = capacity
        self.items = []

    def add(self, item):
        if item is None or item == "":
            raise ValueError(f"List items should not be Empty or Null. But it was [{item}]")
        if item not in self.items:
            self.items.append(item)
            if len(self.items) > self.capacity_value:
                self.items.pop(0)  # Remove the oldest item

    def count(self):
        return len(self.items)

    def capacity(self):
        return self.capacity_value

    def get(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError(f"supplied index [{index}] should be non-negative and not greater than [{len(self.items) - 1}].")
        return self.items[len(self.items) - 1 - index]

    def get_all(self):
        return self.items[::-1]  # Return items in reverse order (most recent first)
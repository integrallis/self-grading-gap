# file: character_copy.py
from candidate import copy_characters


class Copier:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def copy(self):
        return copy_characters(self.source, self.destination)

    def copy_multiple(self, batch_size):
        return copy_characters(self.source, self.destination, batch_size)

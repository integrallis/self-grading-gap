# file: character_copy.py
from candidate.impl import LineBoundedCopier


class Copier:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def copy(self):
        return LineBoundedCopier().copy(self.source, self.destination)

    def copy_multiple(self, batch_size):
        return LineBoundedCopier(batch_size).copy(self.source, self.destination)

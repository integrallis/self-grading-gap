# file: character_copy.py

from candidate.impl import LineBoundedCopier

class Copier:
    def __init__(self, batch_size=None):
        self._copier = LineBoundedCopier(batch_size)

    def copy_one_character(self, source, destination):
        self._copier.copy_one_character(source, destination)

    def copy_in_batches(self, source, destination):
        self._copier.copy_in_batches(source, destination)

    def copy(self, source, destination):
        self._copier.copy(source, destination)

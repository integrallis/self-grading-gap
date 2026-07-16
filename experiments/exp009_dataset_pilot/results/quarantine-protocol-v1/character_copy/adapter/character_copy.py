# file: character_copy.py

from candidate.impl import LineBoundedCopier

class Copier:
    def __init__(self, batch_size=1):
        self._copier = LineBoundedCopier(batch_size)

    def copy_one_character_at_a_time(self, source, destination):
        self._copier.copy_one_character_at_a_time(source, destination)

    def copy_in_batches(self, source, destination):
        self._copier.copy_in_batches(source, destination)

# file: addition_triangulation/addition.py
from candidate.impl import TwoNumberAdder


class Addition:
    of = staticmethod(TwoNumberAdder.add)

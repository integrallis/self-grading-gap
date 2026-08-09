# file: mars_rover.py
from candidate import Rover


_defaults = Rover()


class _Obstacles(set):
    append = set.add


class MarsRover(Rover):
    def __init__(
        self,
        width=_defaults.width,
        height=_defaults.height,
        heading=_defaults.heading,
        obstacles=_defaults.obstacles,
    ):
        Rover.__init__(self, width, height, heading)
        self.obstacles = _Obstacles(obstacles)

    execute = Rover.move

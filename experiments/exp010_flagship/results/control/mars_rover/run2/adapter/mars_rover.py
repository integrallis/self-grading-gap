# file: mars_rover.py
from candidate import Rover


class MarsRover(Rover):
    def execute(self, commands):
        return self.execute_commands(commands)

class Rover:
    def __init__(self, width=0, height=0, heading='N', obstacles=None):
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        self.width = width
        self.height = height
        self.heading = heading.upper()
        self.position = (0, 0)
        self.status = 'ok'
        self.last_obstacle = None
        self.directions = 'NESW'
        self.direction_map = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

        if obstacles is None:
            obstacles = set()
        self.obstacles = obstacles

        if self.heading not in self.directions:
            raise ValueError(f"Unknown direction: {self.heading.lower()}")

    def move(self, commands):
        for command in commands:
            if command == 'f':
                self._move_forward()
            elif command == 'b':
                self._move_backward()
            elif command == 'l':
                self._turn_left()
            elif command == 'r':
                self._turn_right()
            else:
                raise ValueError(f"Unknown command: {command}")

    def _move_forward(self):
        if self.status == 'blocked':
            return
        dx, dy = self.direction_map[self.heading]
        new_x = (self.position[0] + dx) % self.width
        new_y = (self.position[1] + dy) % self.height
        new_position = (new_x, new_y)
        if new_position in self.obstacles:
            self.status = 'blocked'
            self.last_obstacle = new_position
            return
        self.position = new_position
        self.status = 'ok'
        self.last_obstacle = None

    def _move_backward(self):
        if self.status == 'blocked':
            return
        dx, dy = self.direction_map[self.heading]
        new_x = (self.position[0] - dx) % self.width
        new_y = (self.position[1] - dy) % self.height
        new_position = (new_x, new_y)
        if new_position in self.obstacles:
            self.status = 'blocked'
            self.last_obstacle = new_position
            return
        self.position = new_position
        self.status = 'ok'
        self.last_obstacle = None

    def _turn_left(self):
        self.heading = self.directions[(self.directions.index(self.heading) - 1) % 4]

    def _turn_right(self):
        self.heading = self.directions[(self.directions.index(self.heading) + 1) % 4]
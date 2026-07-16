class Rover:
    def __init__(self, width=1, height=1, heading='N'):
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        self.width = width
        self.height = height
        self.heading = self._validate_heading(heading)
        self.position = (0, 0)
        self.status = 'ok'
        self.last_obstacle = None
        self.obstacles = set()

    def _validate_heading(self, heading):
        headings = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
        upper_heading = heading.upper()
        if upper_heading not in headings:
            raise ValueError(f"Unknown direction: {heading}")
        return upper_heading

    def move(self, command):
        if command not in ('f', 'b'):
            raise ValueError(f"Unknown command: {command}")
        dx, dy = self._direction_delta()
        if command == 'b':
            dx, dy = -dx, -dy
        new_x = (self.position[0] + dx) % self.width
        new_y = (self.position[1] + dy) % self.height
        new_position = (new_x, new_y)
        if new_position in self.obstacles:
            self.status = 'blocked'
            self.last_obstacle = new_position
        else:
            self.position = new_position
            self.status = 'ok'
            self.last_obstacle = None

    def _direction_delta(self):
        direction_map = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
        return direction_map[self.heading]

    def turn(self, direction):
        if direction == 'l':
            self.heading = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[self.heading]
        elif direction == 'r':
            self.heading = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[self.heading]

    def execute_commands(self, commands):
        for command in commands:
            if command in ('f', 'b'):
                self.move(command)
            elif command in ('l', 'r'):
                self.turn(command)
            else:
                raise ValueError(f"Unknown command: {command}")

    def add_obstacle(self, position):
        self.obstacles.add(position)
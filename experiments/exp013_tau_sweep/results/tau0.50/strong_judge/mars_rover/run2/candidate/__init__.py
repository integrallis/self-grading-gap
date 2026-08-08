class Rover:
    def __init__(self, width=10, height=10, heading='N'):
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.heading = self.normalize_heading(heading)
        self.obstacles = set()
        self.status = 'ok'
        self.last_obstacle = None

    def normalize_heading(self, heading):
        headings = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        heading = heading.upper()
        if heading not in headings:
            raise ValueError(f"Unknown direction: {heading}")
        return heading

    def move(self, commands):
        for command in commands:
            if command == 'f':
                self.move_forward()
                if self.status == 'blocked':
                    return
            elif command == 'b':
                self.move_backward()
                if self.status == 'blocked':
                    return
            elif command == 'l':
                self.turn_left()
            elif command == 'r':
                self.turn_right()
            else:
                raise ValueError(f"Unknown command: {command}")

    def turn_left(self):
        directions = ['N', 'W', 'S', 'E']
        current_index = directions.index(self.heading)
        self.heading = directions[(current_index + 1) % 4]

    def turn_right(self):
        directions = ['N', 'E', 'S', 'W']
        current_index = directions.index(self.heading)
        self.heading = directions[(current_index + 1) % 4]

    def move_forward(self):
        x, y = self.position
        if self.heading == 'N':
            y = (y - 1) if y > 0 else self.height - 1
        elif self.heading == 'S':
            y = (y + 1) % self.height
        elif self.heading == 'E':
            x = (x + 1) % self.width
        elif self.heading == 'W':
            x = (x - 1) if x > 0 else self.width - 1
        self.check_obstacle((x, y))

    def move_backward(self):
        x, y = self.position
        if self.heading == 'N':
            y = (y + 1) % self.height
        elif self.heading == 'S':
            y = (y - 1) if y > 0 else self.height - 1
        elif self.heading == 'E':
            x = (x - 1) if x > 0 else self.width - 1
        elif self.heading == 'W':
            x = (x + 1) % self.width
        self.check_obstacle((x, y))

    def check_obstacle(self, new_position):
        if new_position in self.obstacles:
            self.status = 'blocked'
            self.last_obstacle = new_position
            return
        self.position = new_position
        self.status = 'ok'
        self.last_obstacle = None

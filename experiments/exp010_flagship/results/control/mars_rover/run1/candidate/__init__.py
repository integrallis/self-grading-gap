class Rover:
    def __init__(self, position=(0, 0), heading='N', grid_size=(100, 100)):
        self.grid_width, self.grid_height = grid_size
        if self.grid_width <= 0 or self.grid_height <= 0:
            raise ValueError('Grid dimensions must be positive')
        self.position = position
        self.heading = heading.upper() if heading.isalpha() else heading
        self.validate_heading()
        self.status = 'ok'
        self.obstacle = None

    def validate_heading(self):
        if self.heading not in ['N', 'E', 'S', 'W']:
            raise ValueError(f'Unknown direction: {self.heading}')

    def set_obstacle(self, position):
        self.obstacle = position

    def execute_commands(self, commands):
        for command in commands:
            if command == 'f':
                self.move_forward()
            elif command == 'b':
                self.move_backward()
            elif command == 'l':
                self.turn_left()
            elif command == 'r':
                self.turn_right()
            else:
                raise ValueError(f'Unknown command: {command}')

    def move_forward(self):
        new_position = self.calculate_new_position(1)
        self.check_obstacle(new_position)

    def move_backward(self):
        new_position = self.calculate_new_position(-1)
        self.check_obstacle(new_position)

    def calculate_new_position(self, direction):
        x, y = self.position
        if self.heading == 'N':
            y = (y + direction) % self.grid_height
        elif self.heading == 'E':
            x = (x + direction) % self.grid_width
        elif self.heading == 'S':
            y = (y - direction) % self.grid_height
        elif self.heading == 'W':
            x = (x - direction) % self.grid_width
        return (x, y)

    def check_obstacle(self, new_position):
        if new_position == self.obstacle:
            self.status = 'blocked'
            return
        self.position = new_position
        self.status = 'ok'
        self.obstacle = None

    def turn_left(self):
        directions = ['N', 'W', 'S', 'E']
        self.heading = directions[(directions.index(self.heading) + 1) % 4]

    def turn_right(self):
        directions = ['N', 'E', 'S', 'W']
        self.heading = directions[(directions.index(self.heading) + 1) % 4]
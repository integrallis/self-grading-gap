class Maze:
    def __init__(self, grid, start, exit):
        self.grid = grid
        self.start = start
        self.exit = exit
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def is_open(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] != '#'


def parse_maze(maze_text):
    lines = maze_text.strip().split('\n')
    grid = [list(line) for line in lines]
    start = None
    exit = None

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == 'S':
                if start is not None:
                    raise ValueError("Maze must contain exactly one start 'S'")
                start = (x, y)
            elif char == 'E':
                if exit is not None:
                    raise ValueError("Maze must contain exactly one exit 'E'")
                exit = (x, y)
            elif char not in {' ', '#', 'S', 'E'}:
                raise ValueError("Unknown maze character")

    if start is None:
        raise ValueError("Maze must contain exactly one start 'S'")
    if exit is None:
        raise ValueError("Maze must contain exactly one exit 'E'")

    return Maze(grid, start, exit)


def solve_maze(maze):
    from collections import deque

    start = maze.start
    exit = maze.exit
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (current, path) = queue.popleft()
        if current == exit:
            return path

        visited.add(current)
        x, y = current

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_position = (x + dx, y + dy)
            if maze.is_open(*next_position) and next_position not in visited:
                queue.append((next_position, path + [next_position]))

    raise ValueError("No path to exit")
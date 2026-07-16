def parse_maze(maze_str):
    maze_lines = maze_str.strip().split('\n')
    height = len(maze_lines)
    width = max(len(line.strip()) for line in maze_lines) if height > 0 else 0
    start = None
    exit = None
    valid_chars = {'#', ' ', 'S', 'E', '.'}

    for y, line in enumerate(maze_lines):
        for x, char in enumerate(line):
            if char not in valid_chars:
                raise ValueError(f"Unknown maze character '{char}' at ({x}, {y})")
            if char == 'S':
                if start is not None:
                    raise ValueError("Maze must contain exactly one start 'S'")
                start = (x, y)
            elif char == 'E':
                if exit is not None:
                    raise ValueError("Maze must contain exactly one exit 'E'")
                exit = (x, y)

    if start is None:
        raise ValueError("Maze must contain exactly one start 'S'")
    if exit is None:
        raise ValueError("Maze must contain exactly one exit 'E'")

    return {'width': width, 'height': height, 'start': start, 'exit': exit}


def solve_maze(maze_str):
    maze = parse_maze(maze_str)
    width, height = maze['width'], maze['height']
    start = maze['start']
    exit = maze['exit']
    path = []
    visited = set()

    def is_valid_move(x, y):
        return 0 <= x < width and 0 <= y < height and (x, y) not in visited and (maze_str.split('\n')[y][x] in ' E.')

    def dfs(x, y):
        if (x, y) == exit:
            path.append((x, y))
            return True
        visited.add((x, y))
        path.append((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if is_valid_move(x + dx, y + dy):
                if dfs(x + dx, y + dy):
                    return True

        path.pop()
        return False

    if not dfs(*start):
        raise ValueError("No path to exit")
    return path
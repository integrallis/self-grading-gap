def parse_maze(maze_text):
    maze = {'cells': {}, 'width': 0, 'height': 0, 'start': None, 'exit': None}
    rows = maze_text.strip().split('\n')
    rows = [row for row in rows if row.strip()]  # Drop blank lines
    maze['height'] = len(rows)
    maze['width'] = max(len(row) for row in rows) if rows else 0

    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            char = char.strip()  # Trim spaces
            if char in ['#', ' ', 'S', 'E', '.']:
                maze['cells'][(x, y)] = char
                if char == 'S':
                    if maze['start'] is not None:
                        raise ValueError("Maze must contain exactly one start 'S'")
                    maze['start'] = (x, y)
                elif char == 'E':
                    if maze['exit'] is not None:
                        raise ValueError("Maze must contain exactly one exit 'E'")
                    maze['exit'] = (x, y)
            else:
                raise ValueError(f"Unknown maze character: {char}")

    if maze['start'] is None:
        raise ValueError("Maze must contain exactly one start 'S'")
    if maze['exit'] is None:
        raise ValueError("Maze must contain exactly one exit 'E'")

    return maze


def solve_maze(maze_text):
    from collections import deque

    maze = parse_maze(maze_text)
    start = maze['start']
    exit = maze['exit']
    queue = deque([start])
    parents = {start: None}
    visited = set([start])

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    while queue:
        current = queue.popleft()
        if current == exit:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]  # return reversed path

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if neighbor in maze['cells'] and neighbor not in visited:
                if maze['cells'][neighbor] in [' ', 'E']:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parents[neighbor] = current

    raise ValueError("No path to exit")
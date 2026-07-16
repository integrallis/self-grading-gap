# file: maze_walker.py
from candidate import Maze
from candidate import parse_maze as _parse_maze
from candidate import solve_maze as walk_maze

Maze.from_text = staticmethod(_parse_maze)

NoPathError = ValueError


class MazeWalker:
    def __init__(self, maze):
        self.maze = maze

    def walk(self):
        return walk_maze(self.maze)

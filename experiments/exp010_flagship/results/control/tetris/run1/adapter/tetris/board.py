# file: tetris/board.py
from candidate import Board as _Board


class Board(_Board):
    move_left = _Board.steer_left
    move_right = _Board.steer_right
    raises = _Board.drop_piece

    def has_falling(self):
        return bool(self.current_piece)

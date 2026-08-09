# file: tic_tac_toe/game.py
from candidate import make_move as _make_move
from candidate import start_game as _start_game


class TicTacToe:
    def __init__(self):
        self.board, self.current_player = _start_game()

    def play(self, row, col):
        self.board, self.current_player = _make_move(
            self.board,
            self.current_player,
            row,
            col,
        )
        return self.board, self.current_player

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['.' for _ in range(cols)] for _ in range(rows)]
        self.falling_piece = None
        self.falling_piece_row = -1
        self.falling_piece_col = -1

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid]) + '\n'

    def drop_block(self, block):
        if self.falling_piece is not None:
            return 'already falling'
        self.falling_piece = Piece([block])
        self.falling_piece_row = 0
        self.falling_piece_col = self.cols // 2
        self.grid[self.falling_piece_row][self.falling_piece_col] = block

    def tick(self):
        if self.falling_piece is None:
            return
        if self.falling_piece_row < self.rows - 1 and self.grid[self.falling_piece_row + 1][self.falling_piece_col] == '.':
            self.grid[self.falling_piece_row][self.falling_piece_col] = '.'
            self.falling_piece_row += 1
            self.grid[self.falling_piece_row][self.falling_piece_col] = self.falling_piece.shape[0][0]
        else:
            self.place_falling_piece()

    def drop_piece(self, piece):
        if self.falling_piece is not None:
            return 'already falling'
        self.falling_piece = piece
        self.falling_piece_row = 0
        self.falling_piece_col = self.cols // 2
        self.update_board_with_piece()

    def update_board_with_piece(self):
        for r in range(len(self.falling_piece.shape)):
            for c in range(len(self.falling_piece.shape[r])):
                if self.falling_piece.shape[r][c] != '.':
                    self.grid[self.falling_piece_row + r][self.falling_piece_col + c] = self.falling_piece.shape[r][c]

    def place_falling_piece(self):
        for r in range(len(self.falling_piece.shape)):
            for c in range(len(self.falling_piece.shape[r])):
                if self.falling_piece.shape[r][c] != '.':
                    self.grid[self.falling_piece_row + r][self.falling_piece_col + c] = self.falling_piece.shape[r][c]
        self.falling_piece = None

    def steer_left(self):
        if self.falling_piece_col > 0:
            self.falling_piece_col -= 1
            if not self.cannot_place_piece():
                self.update_board_with_piece()
            else:
                self.falling_piece_col += 1

    def steer_right(self):
        if self.falling_piece_col + len(self.falling_piece.shape[0]) < self.cols:
            self.falling_piece_col += 1
            if not self.cannot_place_piece():
                self.update_board_with_piece()
            else:
                self.falling_piece_col -= 1

    def rotate_right(self):
        if self.falling_piece:
            temp_shape = self.falling_piece.shape
            self.falling_piece.rotate_right()
            if self.cannot_place_piece():
                self.falling_piece.shape = temp_shape
            self.update_board_with_piece()

    def rotate_left(self):
        if self.falling_piece:
            temp_shape = self.falling_piece.shape
            self.falling_piece.rotate_left()
            if self.cannot_place_piece():
                self.falling_piece.shape = temp_shape
            self.update_board_with_piece()

    def cannot_place_piece(self):
        for r in range(len(self.falling_piece.shape)):
            for c in range(len(self.falling_piece.shape[r])):
                if self.falling_piece.shape[r][c] != '.':
                    row = self.falling_piece_row + r
                    col = self.falling_piece_col + c
                    if row >= self.rows or col < 0 or col >= self.cols or self.grid[row][col] != '.':
                        return True
        return False

class Piece:
    def __init__(self, shape):
        self.shape = shape

    def __str__(self):
        return '\n'.join(self.shape)

    def rotate_right(self):
        self.shape = [''.join(row) for row in zip(*self.shape[::-1])]

    def rotate_left(self):
        self.shape = [''.join(row) for row in zip(*self.shape)][::-1]
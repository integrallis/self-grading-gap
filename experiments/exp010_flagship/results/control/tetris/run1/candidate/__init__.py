class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['.' for _ in range(width)] for _ in range(height)]
        self.current_piece = None
        self.current_piece_row = 0
        self.current_piece_col = 0

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.board])

    def drop(self, block):
        if self.current_piece is not None:
            return 'already falling'
        self.current_piece = block
        self.current_piece_row = 0
        self.current_piece_col = self.width // 2
        self.board[self.current_piece_row][self.current_piece_col] = self.current_piece

    def tick(self):
        if self.current_piece is None:
            return
        next_row = self.current_piece_row + 1
        if next_row < self.height and self.board[next_row][self.current_piece_col] == '.':
            self.board[self.current_piece_row][self.current_piece_col] = '.'
            self.current_piece_row = next_row
            self.board[self.current_piece_row][self.current_piece_col] = self.current_piece
        else:
            self.current_piece = None

    def drop_piece(self, piece):
        piece_height = len(piece.shape)
        piece_width = len(piece.shape[0])
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell == 'T':
                    column_position = (self.width // 2) - (piece_width // 2) + j
                    y_offset = self.height - piece_height
                    while y_offset + i < self.height and self.board[y_offset + i][column_position] == '.':
                        y_offset += 1
                    if y_offset + i - 1 < self.height:
                        self.board[y_offset + i - 1][column_position] = 'T'

    def steer_left(self):
        if self.current_piece is None:
            return
        if self.current_piece_col > 0:
            self.board[self.current_piece_row][self.current_piece_col] = '.'
            self.current_piece_col -= 1
            self.board[self.current_piece_row][self.current_piece_col] = self.current_piece

    def steer_right(self):
        if self.current_piece is None:
            return
        if self.current_piece_col < self.width - 1:
            self.board[self.current_piece_row][self.current_piece_col] = '.'
            self.current_piece_col += 1
            self.board[self.current_piece_row][self.current_piece_col] = self.current_piece

    def rotate_right(self):
        if self.current_piece:
            self.current_piece.rotate_right()

    def rotate_left(self):
        if self.current_piece:
            self.current_piece.rotate_left()

class Piece:
    def __init__(self, shape):
        self.shape = shape

    def __str__(self):
        return '\n'.join(self.shape) + '\n'

    def rotate_right(self):
        self.shape = [''.join(row) for row in zip(*self.shape[::-1])]

    def rotate_left(self):
        self.shape = [''.join(row) for row in zip(*self.shape)][::-1]
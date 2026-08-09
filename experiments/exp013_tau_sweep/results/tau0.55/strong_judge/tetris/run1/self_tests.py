from solution import Board, Piece

def test_board_initialization():
    board = Board(3, 3)
    assert str(board) == '...\n...\n...\n'  # 3x3 board initialized with dots

def test_board_initialization_rectangle():
    board = Board(6, 4)
    assert str(board) == '......\n......\n......\n......\n'  # 6x4 board initialized with dots

def test_board_drop_single_block():
    board = Board(3, 3)
    board.drop_block('X')
    assert str(board) == '.X.\n...\n...\n'  # Block 'X' appears at top middle

def test_board_single_block_falls():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # first tick
    assert str(board) == '...\n.X.\n...\n'  # Block 'X' falls to the middle row
    board.tick()  # second tick
    assert str(board) == '...\n...\n.X.\n'  # Block 'X' reaches the bottom
    board.tick()  # third tick
    assert str(board) == '...\n...\n.X.\n'  # Block 'X' settles at the bottom

def test_board_single_block_lands():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # first tick
    board.tick()  # second tick
    assert str(board) == '...\n...\n.X.\n'  # Block 'X' settles at the bottom

def test_block_falls_through_landed_material():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # first tick
    board.tick()  # second tick
    board.drop_block('O')  # Drop another block
    assert board.drop_block('O') == "already falling"  # Cannot drop while 'X' is falling
    board.tick()  # Move 'O' down
    assert str(board) == '...\n.O.\n.X.\n'  # Block 'O' lands on top of block 'X'

def test_board_prevent_multiple_blocks():
    board = Board(3, 3)
    board.drop_block('X')
    result = board.drop_block('O')  # Attempt to drop another block
    assert result == "already falling"  # Message when trying to drop while already falling

def test_board_piece_shape_rendering():
    piece = Piece(['.X.', 'XXX', '...'])
    assert str(piece) == '.X.\nXXX\n...'  # Piece renders as defined

def test_piece_rotation_right():
    piece = Piece(['.X.', 'XXX', '...'])
    piece.rotate_right()
    assert str(piece) == '...\n.XX\n...'  # Correctly rotated piece

def test_piece_rotation_left():
    piece = Piece(['.X.', 'XXX', '...'])
    piece.rotate_left()
    assert str(piece) == '.X.\nXX.\n...'  # Correctly rotated back to original

def test_piece_rotation_worked_example():
    piece = Piece(['.X.', '.X.', '...'])
    piece.rotate_right()
    assert str(piece) == '...\n.XX\n...'  # Clockwise rotation
    piece.rotate_left()
    assert str(piece) == '.X.\n.X.\n...'  # Counter-clockwise rotation

def test_board_drops_piece():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    assert str(board) == '...T..\n..TTT.\n......\n......\n'  # Piece drops at top middle

def test_board_piece_lands():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    board.tick()  # first tick
    board.tick()  # second tick
    board.tick()  # third tick
    assert str(board) == '......\n......\n...T..\n..TTT.\n'  # Piece settles at the bottom

def test_board_piece_steering_left():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    board.move_left()  # Move piece left
    assert str(board) == '..T...\n.TTT..\n......\n......\n'  # Piece moved left

def test_board_piece_steering_right():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    board.move_right()  # Move piece right
    assert str(board) == '....T.\n...TTT\n......\n......\n'  # Piece moved right

def test_board_piece_lands_on_settled_material():
    board = Board(6, 4)
    board.drop_block('X')
    board.tick()  # first tick
    board.tick()  # second tick
    board.tick()  # third tick
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)  # Drop piece on settled block
    board.tick()  # first tick
    assert str(board) == '......\n......\n...T..\n..TTT.\n'  # Piece settles on top of X

def test_board_piece_transparency():
    board = Board(6, 4)
    board.drop_block('X')  # Drop a block
    board.tick()  # First tick
    piece = Piece(['.X.', 'X..', '...'])  # Drop a piece with transparent cells
    board.drop_piece(piece)
    assert str(board) == '...X..\n...X..\n......\n......\n'  # Pieces are rendered with transparency

def test_board_piece_no_room_to_fall():
    board = Board(6, 4)
    board.drop_block('X')
    board.tick()  # first tick
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    assert str(board) == '......\n......\n..T..\n.TTT.\n'  # Piece in initial position
    assert board.tick() == "already falling"  # Piece does not descend

def test_board_piece_clipping():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    board.move_right()  # Move piece right
    assert str(board) == '......\n......\n...T..\n..TTT.\n'  # Piece visible without clipping

def test_single_block_move_left():
    board = Board(6, 4)
    board.drop_block('X')
    board.tick()  # first tick
    board.move_left()
    assert str(board) == '......\n..X...\n......\n......\n'  # Block moved left

def test_single_block_move_right():
    board = Board(6, 4)
    board.drop_block('X')
    board.tick()  # first tick
    board.move_right()
    assert str(board) == '......\n....X.\n......\n......\n'  # Block moved right

def test_move_left_boundary():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # first tick
    board.move_left()  # Move left
    board.move_left()  # Should stay in place due to boundary
    assert str(board) == '...\n.X.\n...\n'  # Block remains in original position

def test_move_right_boundary():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # first tick
    board.move_right()  # Move right
    board.move_right()  # Should stay in place due to boundary
    assert str(board) == '...\n.X.\n...\n'  # Block remains in original position

def test_nothing_falling_move():
    board = Board(3, 3)
    board.move_left()  # should leave the board unchanged
    assert str(board) == '...\n...\n...\n'  # Board remains empty

def test_nothing_falling_rotate():
    board = Board(3, 3)
    board.rotate_right()  # should leave the board unchanged
    assert str(board) == '...\n...\n...\n'  # Board remains empty

def test_rotate_single_block():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # first tick
    board.rotate_right()  # should keep the block the same
    assert str(board) == '...\n.X.\n...\n'  # Block remains unchanged

def test_board_piece_rotation_success():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    board.rotate_right()  # Rotate piece right
    assert str(board) == '......\n..TT..\n...T..\n......\n'  # Piece rotated

    board.rotate_left()  # Rotate piece left
    assert str(board) == '...T..\n..TTT.\n......\n......\n'  # Piece returned to original position

def test_board_piece_rotation_fail():
    board = Board(6, 4)
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)
    board.move_left()  # Move piece left
    board.rotate_right()  # Attempt to rotate
    assert str(board) == '..T...\n.TTT..\n......\n......\n'  # Rotation fails, board unchanged

def test_board_piece_lands_on_settled_material():
    board = Board(6, 4)
    board.drop_block('X')
    board.tick()  # first tick
    board.tick()  # second tick
    piece = Piece(['..T..', '.TTT.'])
    board.drop_piece(piece)  # Drop piece on settled block
    board.tick()  # Move piece down
    assert str(board) == '......\n......\n...T..\n..TTT.\n'  # Piece settles on top of X
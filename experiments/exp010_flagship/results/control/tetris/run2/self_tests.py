from solution import Board, Piece

def test_board_initialization():
    board = Board(3, 3)
    # A 3x3 board should render as three rows of "..."
    expected_output = "...\n...\n...\n"
    assert str(board) == expected_output

def test_drop_single_block():
    board = Board(3, 3)
    board.drop('A')
    # After dropping block 'A', it should be at the top middle (1,0)
    expected_output = "...  \n.A.\n...\n"  # Note: ensure no trailing space
    assert str(board) == expected_output

def test_block_falls():
    board = Board(3, 3)
    board.drop('A')
    board.tick()  # First tick, block should move down
    expected_output = "...  \n.A.\n...\n"  # No change yet
    assert str(board) == expected_output
    board.tick()  # Second tick, block should move down again
    expected_output = "...  \n...\n.A.\n"  # Block moves down
    assert str(board) == expected_output

def test_block_lands():
    board = Board(3, 3)
    board.drop('A')
    board.tick()  # First tick
    board.tick()  # Second tick, block should land
    expected_output = "...  \n...\n.A.\n"  # Block is settled
    assert str(board) == expected_output

def test_block_stops_at_bottom():
    board = Board(3, 3)
    board.drop('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Third tick, block should land
    board.tick()  # Fourth tick, nothing should move
    expected_output = "...  \n...\n.A.\n"  # Block is settled
    assert str(board) == expected_output

def test_multiple_blocks_cannot_fall():
    board = Board(3, 3)
    board.drop('A')
    assert board.drop('B') == "already falling"

def test_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop('A')
    board.tick()
    board.tick()  # 'A' lands
    board.drop('B')  # Drop another block
    board.tick()  # 'B' should land on 'A'
    expected_output = "...  \n.B.\n.A.\n"  # Block B on top of A
    assert str(board) == expected_output

def test_piece_initialization():
    piece = Piece([".T.", "TTT", "..."])
    # A T-shape piece should render as defined
    expected_output = ".T.\nTTT\n...\n"
    assert str(piece) == expected_output

def test_piece_rotation_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    # Rotating right should give rows "...", ".XX", "..."
    expected_output = "...\nXX.\n...\n"
    assert str(piece) == expected_output

def test_piece_rotation_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    # Rotating left should give rows "...", ".XX", "..."
    expected_output = "...\nXX.\n...\n"
    assert str(piece) == expected_output

def test_drop_piece_centered_on_board():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    # Piece should be centered; on a 6-wide board it should be "....T.." and "..TTT.."
    expected_output = "......\n......\n....T.\n..TTT.\n"
    assert str(board) == expected_output

def test_piece_lands_on_board():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Third tick
    board.tick()  # Fourth tick
    expected_output = "......\n......\n......\n....T.\n..TTT.\n"
    assert str(board) == expected_output

def test_piece_lands_keeping_shape():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.tick()  # Move down
    board.move_left()  # Move left
    board.tick()  # Move down again
    expected_output = "......\n......\n...T..\n.TTT..\n"
    assert str(board) == expected_output

def test_move_piece_left():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.move_left()  # Move piece left
    expected_output = "......\n......\n...T..\n.TTT..\n"
    assert str(board) == expected_output

def test_move_piece_right():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.move_right()  # Move piece right
    expected_output = "......\n......\n....T.\n..TTT.\n"
    assert str(board) == expected_output

def test_move_piece_out_of_bounds():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.move_left()  # Move left
    board.move_left()  # Move left again
    expected_output = "......\n......\n...T..\n.TTT..\n"
    assert str(board) == expected_output

def test_rotate_piece_when_falling():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.rotate_right()  # Rotate right
    expected_output = "......\n......\n..T...\n..TTT.\n"
    assert str(board) == expected_output

def test_abandon_rotation_if_blocked():
    board = Board(6, 4)
    piece = Piece(["..T...", ".TTT..", "......"])
    board.drop(piece)
    board.tick()  # Move down
    board.move_left()  # Move left
    board.rotate_right()  # Attempt to rotate
    expected_output = "......\n......\n...T..\n.TTT..\n"
    assert str(board) == expected_output

def test_piece_immediate_land_if_no_room():
    board = Board(3, 3)
    piece = Piece(["XXX", "XXX", "XXX"])  # Full piece
    board.drop(piece)  # Should land immediately
    expected_output = "XXX\nXXX\nXXX\n"  # Immediate landing
    assert str(board) == expected_output

def test_piece_clipping():
    board = Board(3, 3)
    piece = Piece(["..X", "XX.", "X.."])  # Partially off the board
    board.drop(piece)
    board.tick()  # Should not clip and land correctly
    expected_output = "...\n.XX\nX..\n"  # Only visible parts
    assert str(board) == expected_output
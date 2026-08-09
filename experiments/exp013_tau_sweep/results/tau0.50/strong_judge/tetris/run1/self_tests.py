from solution import Board, Piece

def test_board_initialization():
    board = Board(3, 3)
    expected_output = "...\n...\n...\n"  # 3 rows of 3 dots
    assert str(board) == expected_output

def test_dropping_single_block():
    board = Board(3, 3)
    board.drop_block('A')
    expected_output = ".A.\n...\n...\n"  # Block 'A' in the middle of the top row
    assert str(board) == expected_output

def test_single_block_falls_one_row():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    expected_output = "... \n.A.\n...\n"  # Block 'A' has fallen one row
    assert str(board) == expected_output

def test_single_block_lands():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    expected_output = "... \n...\n.A.\n"  # Block 'A' is now landed at the bottom
    board.tick()  # Next tick should allow dropping another block
    assert str(board) == expected_output
    
    result = board.drop_block('B')  # Attempt to drop another block
    assert result == "already falling"  # Should not be refused

def test_falling_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick to land 'A'
    board.tick()  # Next tick should settle 'A'
    board.drop_block('B')  # Now drop block 'B'
    expected_output = "... \n.A.\n.B.\n"  # Block 'B' should land on 'A'
    board.tick()  # Final tick to settle 'B'
    assert str(board) == expected_output

def test_piece_initialization():
    piece = Piece([".T.", "TTT", "..."])  # T-shape
    expected_output = ".T.\nTTT\n...\n"  # Shape should render as defined
    assert str(piece) == expected_output

def test_dropping_piece():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    expected_output = "...T..\n..TTT.\n......\n......\n"  # T-shape in the center of the board
    assert str(board) == expected_output

def test_piece_falls_one_row():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # First tick
    expected_output = "......\n...T..\n..TTT.\n......\n"  # Piece should have fallen one row
    assert str(board) == expected_output

def test_piece_lands():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # First tick
    board.tick()  # Second tick
    expected_output = "......\n......\n...T..\n..TTT.\n"  # Piece lands
    board.tick()  # Next tick should allow dropping another piece
    assert str(board) == expected_output
    
    result = board.drop_piece(Piece([".T.", "TTT", "..."]))  # Attempt to drop another piece
    assert result == "already falling"  # Should refuse to drop another piece

def test_piece_with_no_room_to_fall_lands_immediately():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # Let 'A' land
    piece = Piece(["AAA", "..."])
    result = board.drop_piece(piece)  # Dropping a piece that cannot fit
    assert result == "already falling"  # Should refuse to drop another piece

def test_steering_falling_piece_left():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.move_left()  # Move the piece left
    expected_output = "......\n..T...\n..TTT.\n......\n"  # Piece should move left
    assert str(board) == expected_output

def test_steering_falling_piece_right():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.move_right()  # Move the piece right
    expected_output = "......\n...T..\n..TTT.\n......\n"  # Piece should move right
    assert str(board) == expected_output

def test_steering_piece_at_boundary_does_not_move():
    board = Board(3, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.move_left()  # Move left
    board.move_left()  # Move left again (should not move)
    expected_output = ".T.\nTTT\n...\n"  # Should remain in the original position
    assert str(board) == expected_output

def test_rotating_falling_piece():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.rotate_right()  # Rotate piece clockwise
    expected_output = "......\n...T..\n...TT.\n......\n"  # Should rotate correctly
    assert str(board) == expected_output

def test_rotating_piece_that_cannot_fit_does_not_change_board():
    board = Board(3, 3)
    piece = Piece(["TT", "TT"])
    board.drop_piece(piece)
    board.rotate_right()  # Attempt to rotate piece
    expected_output = ".TT\n.TT\n...\n"  # Should remain the same
    assert str(board) == expected_output

def test_piece_lands_on_previous_material():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Settle 'A'
    piece = Piece([".T.", "TTT", "..."])  # T-piece
    board.drop_piece(piece)  # Drops T-piece
    expected_output = ".T.\nTTT\n.A.\n"  # T-piece should land on top of 'A'
    assert str(board) == expected_output

def test_clipping_right_edge():
    board = Board(6, 4)
    piece = Piece(["..T.", "TTT", "..."])  # T-piece with part extending beyond right
    board.drop_piece(piece)
    expected_output = "......\n...T..\n..TTT.\n......\n"  # Clipped piece
    assert str(board) == expected_output

def test_clipping_bottom_edge():
    board = Board(3, 3)
    piece = Piece(["A..", "A.."])  # Piece that would extend beyond bottom
    board.drop_piece(piece)  # Drops piece
    expected_output = "A..\nA..\n...\n"  # Should remain unchanged
    assert str(board) == expected_output

def test_steering_single_block():
    board = Board(3, 3)
    board.drop_block('B')
    board.move_left()  # Move left
    expected_output = "B..\n...\n...\n"  # Block B should move left
    assert str(board) == expected_output

def test_no_move_when_nothing_is_falling():
    board = Board(3, 3)
    board.move_left()  # Move left when nothing is falling
    expected_output = "...\n...\n...\n"  # Board should remain unchanged
    assert str(board) == expected_output

def test_rotating_single_block():
    board = Board(3, 3)
    board.drop_block('C')
    board.rotate_right()  # Rotate single block
    expected_output = ".C.\n...\n...\n"  # Block C should remain unchanged
    assert str(board) == expected_output
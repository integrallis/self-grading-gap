from solution import Board, Piece

def test_board_initialization():
    board = Board(3, 3)
    expected = "...\n...\n...\n"  # 3 rows of 3 dots
    assert str(board) == expected

def test_single_block_drops():
    board = Board(3, 3)
    board.drop_block('A')
    expected = ".A.\n...\n...\n"  # Block 'A' in the top middle
    assert str(board) == expected

def test_single_block_falls():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    expected = "...\n.A.\n...\n"  # Block 'A' falling
    assert str(board) == expected

def test_single_block_lands():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    expected = "...\n...\n.A.\n"  # Block 'A' landed
    assert str(board) == expected

def test_block_reaches_bottom():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Third tick
    expected = "...\n...\n.A.\n"  # Block 'A' at bottom
    assert str(board) == expected

def test_block_stops_at_bottom():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Third tick
    board.tick()  # Fourth tick, should not change
    expected = "...\n...\n.A.\n"  # Block 'A' should not fall further
    assert str(board) == expected

def test_only_one_block_can_fall():
    board = Board(3, 3)
    board.drop_block('A')
    result = board.drop_block('B')  # Attempt to drop another block
    expected_message = "already falling"
    assert result == expected_message

def test_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # First tick
    board.tick()  # Second tick
    result = board.drop_block('B')  # Attempt to drop another block
    expected = "...\n.B.\n.A.\n"  # Block 'B' should land on 'A'
    assert str(board) == expected
    assert result == "already falling"

def test_piece_definition_and_rendering():
    piece = Piece([".T.", "TTT", "..."])
    expected = ".T.\nTTT\n...\n"  # Piece should render as defined
    assert str(piece) == expected

def test_piece_rotation_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    expected = ["...", ".XX", "..."]  # After rotating right
    assert str(piece) == "\n".join(expected) + "\n"

def test_piece_rotation_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    expected = ["...", "XX.", "..."]  # After rotating left
    assert str(piece) == "\n".join(expected) + "\n"

def test_t_shape_rendering():
    piece = Piece([".T.", "TTT", "..."])
    expected = ".T.\nTTT\n...\n"  # Stock T-shape
    assert str(piece) == expected

def test_piece_drops_on_board():
    board = Board(7, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    expected = "....T..\n...TTT.\n.......\n.......\n.......\n"  # Piece centered
    assert str(board) == expected

def test_piece_lands_on_board():
    board = Board(7, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    for _ in range(3):  # Simulate 3 ticks
        board.tick()
    expected = ".......\n.......\n.......\n....T..\n...TTT.\n"  # Piece at the bottom
    assert str(board) == expected

def test_piece_lands_when_no_space_to_fall():
    board = Board(3, 3)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    expected = ".X.\nXXX\n...\n"  # Piece lands immediately
    assert str(board) == expected

def test_piece_steering_left():
    board = Board(5, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_left()  # Move piece left
    expected = ".T...\nTTT..\n.....\n.....\n.....\n"  # Piece moved left
    assert str(board) == expected

def test_piece_steering_right():
    board = Board(5, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_right()  # Move piece right
    expected = "...T.\n..TTT\n.....\n.....\n.....\n"  # Piece moved right
    assert str(board) == expected

def test_piece_rotation_around_landed_material():
    board = Board(3, 3)
    piece = Piece([".X.", "X.X", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.tick()  # Move piece down
    board.drop_block('A')  # Add landed material
    board.rotate_right()  # Attempt to rotate
    expected = "...\n.X.\nXXX\n"  # Piece should not rotate
    assert str(board) == expected

def test_piece_stops_on_landed_material():
    board = Board(5, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    for _ in range(3):  # Simulate 3 ticks
        board.tick()
    board.drop_block('X')  # Place a block on the bottom
    expected = ".....\n.....\n.....\n....T.\n...TTT\n"  # T-piece should land above X
    assert str(board) == expected

def test_piece_drops_after_block():
    board = Board(5, 5)
    board.drop_block('A')
    for _ in range(3):  # Simulate 3 ticks
        board.tick()
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    expected = ".....\n.....\n.....\n....A.\n...TTT\n"  # Piece should be dropped after block
    assert str(board) == expected

def test_piece_immediate_landing():
    board = Board(3, 3)
    piece = Piece(["XXX", "XXX", "XXX"])
    board.drop_piece(piece)
    expected = "XXX\nXXX\nXXX\n"  # Piece should land immediately
    assert str(board) == expected

def test_piece_clipping_right():
    board = Board(6, 3)
    piece = Piece(["..X..", "..X..", "XXXXX"])
    board.drop_piece(piece)
    expected = ".....\n.....\nXXXXX\n"  # Piece clipped at right edge
    assert str(board) == expected

def test_piece_clipping_bottom():
    board = Board(3, 3)
    piece = Piece(["X", "X", "X", "X"])
    board.drop_piece(piece)
    expected = "X\nX\nX\n"  # Piece clipped at bottom
    assert str(board) == expected

def test_steering_rejects_boundary():
    board = Board(5, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_left()  # Move piece left
    board.steer_left()  # Move piece left again, should be rejected
    expected = ".T...\nTTT..\n.....\n.....\n.....\n"  # Piece should remain in place
    assert str(board) == expected

def test_steering_single_block():
    board = Board(5, 5)
    board.drop_block('A')
    board.steer_left()  # Attempt to steer left
    expected = ".A.\n...\n...\n...\n...\n"  # Block should move left
    assert str(board) == expected

def test_move_and_rotate_when_nothing_falling():
    board = Board(5, 5)
    board.steer_left()  # Should not change the board
    board.rotate_right()  # Should not change the board
    expected = ".....\n.....\n.....\n.....\n.....\n"  # Board remains unchanged
    assert str(board) == expected

def test_piece_lands_when_no_space_to_fall():
    board = Board(3, 3)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    expected = ".X.\nXXX\n...\n"  # Piece lands immediately
    assert str(board) == expected

def test_piece_land_after_steering():
    board = Board(5, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_left()  # Move piece left
    for _ in range(2):  # Simulate 2 ticks
        board.tick()
    expected = ".....\n.T..\nTTT.\n.....\n.....\n"  # Piece landed after steering
    assert str(board) == expected

def test_piece_rotation_success():
    board = Board(5, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    for _ in range(2):  # Simulate 2 ticks
        board.tick()
    board.rotate_right()  # Rotate the piece
    expected = ".....\n..TT.\n..T..\n.....\n.....\n"  # Piece rotated
    assert str(board) == expected

def test_piece_rotation_rejects_landing():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    for _ in range(2):  # Simulate 2 ticks
        board.tick()
    board.drop_block('A')  # Place a block below
    board.rotate_right()  # Attempt to rotate
    expected = ".....\n.X.\nXXX\nA....\n.....\n"  # Should not change due to block
    assert str(board) == expected

def test_single_block_stays_falling():
    board = Board(5, 5)
    board.drop_block('A')
    for _ in range(4):  # Simulate 4 ticks
        board.tick()
    result = board.drop_block('B')  # Attempt to drop another block
    expected = ".....\n.....\n.....\n..A..\n.....\n"  # Block 'A' should still be falling
    assert str(board) == expected
    assert result == "already falling"
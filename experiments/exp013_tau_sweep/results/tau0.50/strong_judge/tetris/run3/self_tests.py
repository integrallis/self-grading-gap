from solution import Board, Piece

def test_empty_board_rendering():
    board = Board(3, 3)
    expected_rendering = "...\n...\n...\n"  # 3 rows of dots for a 3x3 board
    assert str(board) == expected_rendering

def test_board_dimensions():
    board = Board(6, 4)
    assert len(str(board).splitlines()) == 4  # Height of the board
    assert all(len(row) == 6 for row in str(board).splitlines())  # Width of the board

def test_drop_single_block():
    board = Board(3, 3)
    board.drop_block('X')
    expected_rendering = ".X.\n...\n...\n"  # 'X' appears at the top middle
    assert str(board) == expected_rendering

def test_single_block_falls_one_row():
    board = Board(3, 3)
    board.drop_block('X')  # Drop the block
    board.tick()  # Simulate one tick
    expected_rendering = "... \n.X.\n...\n"  # Block is still falling
    assert str(board) == expected_rendering
    board.tick()  # Simulate another tick
    expected_rendering = "... \n...\n.X.\n"  # Block has landed
    assert str(board) == expected_rendering

def test_block_lands_on_bottom():
    board = Board(3, 3)
    board.drop_block('X')  # Drop the block
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Third tick
    expected_rendering = "... \n... \n.X.\n"  # Block at bottom
    assert str(board) == expected_rendering
    board.tick()  # Block should stop here
    expected_rendering = "... \n... \nX..\n"  # Final landing position
    assert str(board) == expected_rendering

def test_cannot_drop_block_when_one_is_falling():
    board = Board(3, 3)
    board.drop_block('X')
    result = board.drop_block('Y')  # Attempt to drop another block
    assert result == "already falling"

def test_block_stops_on_landed_blocks():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # First tick
    board.tick()  # Second tick
    board.tick()  # Block should be at the bottom center
    board.drop_block('Y')  # Attempt to drop another block on the first block
    assert board.drop_block('Y') == "already falling"  # 'Y' should not be able to drop
    board.tick()  # 'Y' lands on 'X'
    expected_rendering = "... \nX..\nY..\n"  # 'Y' should land on top of 'X'
    assert str(board) == expected_rendering

def test_define_and_render_piece():
    piece = Piece([".T.", "TTT", "..."])
    expected_rendering = ".T.\nTTT\n...\n"  # Piece shape rendering
    assert str(piece) == expected_rendering

def test_rotating_piece_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    expected_rendering = ["...", ".XX", "..."]  # Rotated shape
    assert str(piece) == "\n".join(expected_rendering) + "\n"

def test_rotating_piece_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    expected_rendering = ["...", "XX.", "..."]  # Rotated shape
    assert str(piece) == "\n".join(expected_rendering) + "\n"

def test_drop_piece_on_board():
    board = Board(6, 4)
    piece = Piece(["..T..", ".TTT.", "....."])
    board.drop_piece(piece)
    expected_rendering_6 = "......\n......\n..T...\n.TTT..\n"  # Piece at top center of 6-wide board
    assert str(board) == expected_rendering_6
    
    piece = Piece(["...T..", ".TTT.", "......"])
    board = Board(7, 4)
    board.drop_piece(piece)
    expected_rendering_7 = ".......\n.......\n...T..\n..TTT.\n"  # Piece at top center of 7-wide board
    assert str(board) == expected_rendering_7

def test_falling_piece_descends():
    board = Board(5, 5)
    piece = Piece(["..T..", ".TTT.", "....."])
    board.drop_piece(piece)
    board.tick()  # Move piece down one
    expected_rendering = "......\n......\n......\n..T...\n.TTT..\n"
    assert str(board) == expected_rendering

def test_piece_lands_on_bottom():
    board = Board(5, 5)
    piece = Piece(["..T..", ".TTT.", "....."])
    board.drop_piece(piece)
    for _ in range(3):
        board.tick()  # Move down
    expected_rendering = "......\n......\n......\n......\n..T...\n.TTT..\n"
    assert str(board) == expected_rendering

def test_piece_cannot_move_beyond_side_boundary():
    board = Board(5, 5)
    piece = Piece(["..T..", ".TTT.", "....."])
    board.drop_piece(piece)
    board.move_left()  # Move left
    board.move_left()  # Move left
    board.move_left()  # Should not move past boundary
    expected_rendering = "......\n......\n......\n..T...\n.TTT..\n"
    assert str(board) == expected_rendering

def test_rotate_falling_piece():
    board = Board(5, 5)
    piece = Piece([".X.", ".X.", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.rotate_right()  # Rotate piece in place
    expected_rendering = "......\n......\n......\n.X...\n.XX..\n"
    assert str(board) == expected_rendering

def test_rotation_abandoned_if_blocked():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.tick()  # Move down
    board.rotate_right()  # Attempt to rotate, but blocked
    expected_rendering = "......\n......\n......\n.X...\nXXX.\n"
    assert str(board) == expected_rendering

def test_block_and_piece_can_land_successively():
    board = Board(5, 5)
    board.drop_block('X')  # Drop a block
    for _ in range(3):
        board.tick()  # Move down
    board.drop_piece(Piece(["..T..", ".TTT.", "....."]))  # Drop a piece on top
    expected_rendering = "......\n......\n......\n.X...\n.TTT.\n"
    assert str(board) == expected_rendering

def test_piece_with_transparency():
    board = Board(5, 5)
    piece = Piece(["..T..", ".TTT.", "....."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    expected_rendering = "......\n......\n......\n..T...\n.TTT..\n"  # Transparent cells should show empty space
    assert str(board) == expected_rendering

def test_piece_with_no_room_to_fall():
    board = Board(5, 5)
    piece = Piece(["TTT", "TTT", "..."])  # A piece that cannot fit
    board.drop_piece(piece)
    expected_rendering = "TTT..\nTTT..\n.....\n.....\n.....\n"  # Piece should settle immediately
    assert str(board) == expected_rendering

def test_right_edge_clipping():
    board = Board(5, 5)
    piece = Piece(["...T.", ".TT..", "....."])  # Piece with a right edge that will be clipped
    board.drop_piece(piece)
    board.tick()  # Move down
    expected_rendering = "......\n......\n......\n...T.\n..TT.\n"  # Right edge clipped
    assert str(board) == expected_rendering

def test_bottom_edge_clipping():
    board = Board(5, 5)
    piece = Piece(["..T..", ".TTT.", "TTT.."])  # Piece that exceeds the bottom
    board.drop_piece(piece)
    for _ in range(3):
        board.tick()  # Move down
    expected_rendering = "......\n......\n......\n..T..\n.TTT.\n"  # Bottom edge clipped
    assert str(board) == expected_rendering

def test_move_falling_block_left():
    board = Board(5, 5)
    board.drop_block('X')
    board.tick()  # Move down
    board.move_left()  # Move left
    expected_rendering = "......\n......\n......\n.X...\n.....\n"  # Block moved left
    assert str(board) == expected_rendering

def test_move_falling_block_right():
    board = Board(5, 5)
    board.drop_block('X')
    board.tick()  # Move down
    board.move_right()  # Move right
    expected_rendering = "......\n......\n......\n...X.\n.....\n"  # Block moved right
    assert str(board) == expected_rendering

def test_move_falling_block_right_boundary():
    board = Board(5, 5)
    board.drop_block('X')
    for _ in range(3):
        board.tick()  # Move down
    board.move_right()  # Attempt to move right, should not move
    expected_rendering = "......\n......\n......\n.X...\n.....\n"  # Block should remain
    assert str(board) == expected_rendering

def test_move_and_rotate_when_nothing_falling():
    board = Board(5, 5)
    board.move_left()  # No falling object, so should do nothing
    board.rotate_right()  # No falling object, so should do nothing
    expected_rendering = "......\n......\n......\n......\n......\n"  # Board remains unchanged
    assert str(board) == expected_rendering

def test_rotate_falling_single_block():
    board = Board(5, 5)
    board.drop_block('X')
    board.tick()  # Move down
    board.rotate_right()  # Rotating a block doesn't change its state or shape
    expected_rendering = "......\n......\n......\n.X...\n.....\n"  # Block remains the same
    assert str(board) == expected_rendering

def test_new_board_has_no_falling_object():
    board = Board(3, 3)
    assert board.is_falling() == False  # No block should be falling

def test_drop_block_after_landing():
    board = Board(3, 3)
    board.drop_block('X')
    for _ in range(2):
        board.tick()  # Move down
    board.tick()  # Settle block
    assert board.drop_block('Y') == None  # Should allow dropping another block

def test_drop_single_block_starting_column():
    board = Board(6, 4)
    board.drop_block('X')
    expected_rendering = "......\n......\n...X..\n......\n"  # 'X' appears at the top middle (4th column in a 6-wide board)
    assert str(board) == expected_rendering
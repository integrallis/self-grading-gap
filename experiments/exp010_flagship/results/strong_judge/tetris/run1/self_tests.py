from solution import *

def test_board_initialization_3x3():
    board = Board(3, 3)
    assert str(board) == "...\n...\n...\n"

def test_board_initialization_empty_6x4():
    board = Board(6, 4)
    assert str(board) == "......\n......\n......\n......\n"

def test_drop_single_block_initial_3x3():
    board = Board(3, 3)
    block = Block('X')
    board.drop_block(block)
    assert str(board) == ".X.\n...\n...\n"

def test_drop_single_block_middle_6x4():
    board = Board(6, 4)
    block = Block('X')
    board.drop_block(block)
    assert str(board) == "......\n......\n...X..\n......\n"  # 6-wide board, block in row 2, column 3

def test_tick_single_block_falls_3x3():
    board = Board(3, 3)
    block = Block('X')
    board.drop_block(block)
    board.tick()  # First tick
    assert str(board) == "...\n.X.\n...\n"  # Block falls to row 1
    board.tick()  # Second tick
    assert str(board) == "...\n...\n.X.\n"  # Block falls to row 2

def test_block_lands_at_bottom_3x3():
    board = Board(3, 3)
    block = Block('X')
    board.drop_block(block)
    board.tick()  # Falls to row 1
    board.tick()  # Falls to row 2
    board.tick()  # Should land
    assert str(board) == "...\n...\n.X.\n"  # Block is settled at the bottom

def test_cannot_drop_block_while_falling_3x3():
    board = Board(3, 3)
    block1 = Block('X')
    block2 = Block('O')
    board.drop_block(block1)
    result = board.drop_block(block2)  # Attempt to drop second block while one is falling
    assert result == "already falling"  # Must return the refusal message
    assert str(board) == "...\n...\n.X.\n"  # Board state remains unchanged

def test_block_stops_on_landed_block_3x3():
    board = Board(3, 3)
    block1 = Block('X')
    block2 = Block('O')
    board.drop_block(block1)
    board.tick()  # Block1 falls to row 1
    board.tick()  # Block1 falls to row 2
    board.tick()  # Let Block1 settle
    assert str(board) == "...\n...\n.X.\n"  # Block1 is settled
    board.drop_block(block2)  # Block2 should now attempt to fall
    board.tick()  # Block2 should fall to row 1
    assert str(board) == "...\n.O.\n.X.\n"  # Block2 is above Block1

def test_drop_piece_initial_6x4():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    assert str(board) == "......\n......\n...T..\n..TTT.\n"  # Piece is centered

def test_width_7_drop_piece_initial():
    board = Board(7, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    assert str(board) == "....T..\n...TTT.\n.......\n.......\n"  # Piece is centered

def test_piece_falls_6x4():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Piece falls
    assert str(board) == "......\n......\n......\n...T..\n..TTT.\n"  # Piece has fallen one row

def test_piece_lands_on_bottom_6x4():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    for _ in range(2):  # Let it fall to the bottom
        board.tick()
    board.tick()  # Settle the piece
    assert str(board) == "......\n......\n...T..\n..TTT.\n"  # Piece is settled at the bottom

def test_piece_cannot_overlap():
    board = Board(3, 3)
    piece1 = Piece(["X"])
    piece2 = Piece(["X"])
    board.drop_piece(piece1)
    for _ in range(2):
        board.tick()  # Let piece1 fall
    board.drop_piece(piece2)  # Piece2 should attempt to land on piece1
    board.tick()  # Attempt to settle Piece2
    assert str(board) == "...\n.X.\n.X.\n"  # Piece2 can't overlap Piece1

def test_steer_piece_left():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # First tick
    board.steer_left()
    assert str(board) == "......\n......\n..T...\n..TTT.\n"  # Piece moved left

def test_steer_piece_right():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # First tick
    board.steer_right()
    assert str(board) == "......\n......\n....T.\n...TTT\n"  # Piece moved right

def test_steer_piece_cannot_cross_boundaries():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # First tick
    board.steer_right()  # First move right is legal
    board.steer_right()  # Second move right is legal
    board.steer_right()  # Third move right is legal
    board.steer_right()  # Fourth move right is legal
    board.steer_right()  # Fifth move right is blocked
    assert str(board) == "......\n......\n....T.\n...TTT\n"  # Blocked on the right

def test_rotate_piece():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # First tick
    board.rotate_right()
    assert str(board) == "......\n......\n...TT.\n...T..\n"  # Rotated piece

def test_rotate_piece_cannot_overlap():
    board = Board(6, 4)
    piece1 = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece1)
    for _ in range(2):  # Let it fall to the bottom
        board.tick()
    block = Block('X')
    board.drop_block(block)  # Place a block underneath
    result = board.rotate_right()  # Should not rotate due to overlap
    assert str(board) == "......\n......\n...T..\n..TTT.\n"  # Board unchanged

def test_rotate_block_has_no_effect():
    board = Board(3, 3)
    block = Block('X')
    board.drop_block(block)
    board.rotate_right()  # Should do nothing
    assert str(board) == ".X.\n...\n...\n"  # Block state unchanged
    board.tick()  # Verify that the block continues to fall
    assert str(board) == "...\n.X.\n...\n"

def test_rotate_piece_cannot_rotate_into_block():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    for _ in range(2):  # Let it fall to the bottom
        board.tick()
    block = Block('X')
    board.drop_block(block)  # Place a block underneath
    result = board.rotate_right()  # Should not rotate due to overlap
    assert str(board) == "......\n......\n...T..\n..TTT.\n"  # Board unchanged

def test_piece_with_no_room_lands_immediately():
    board = Board(3, 3)
    piece = Piece(["XXX", "XXX", "XXX"])
    board.drop_piece(piece)
    assert str(board) == "XXX\nXXX\nXXX\n"  # Piece fills the board immediately

def test_piece_transparency():
    board = Board(6, 4)
    piece = Piece([".X.", "XXX", ".X."])
    board.drop_piece(piece)
    board.tick()  # Let it fall
    board.tick()  # Let it fall
    board.tick()  # Let it fall
    board.tick()  # Settle the piece
    assert str(board) == "......\n......\n.X...\nXXXXX\n"  # Transparency shows landed material

def test_clip_right_edge():
    board = Board(6, 4)
    piece = Piece(["X....", "XX...", "X...."])
    board.drop_piece(piece)
    board.tick()  # Let it fall
    assert str(board) == "......\n......\n......\nX....\nXX...\n"  # Clipped at the right edge

def test_clip_bottom_edge():
    board = Board(3, 3)
    piece = Piece(["X", "X", "X"])
    board.drop_piece(piece)
    assert str(board) == ".X.\n.X.\n.X.\n"  # Piece is centered vertically
    board.drop_piece(piece)  # Try to drop another piece
    assert str(board) == ".X.\n.X.\n.X.\n"  # Should remain unchanged as no space
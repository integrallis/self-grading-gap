from solution import Board, Piece

# US-1: See the board
def test_empty_board():
    board = Board(3, 3)
    assert str(board) == "...\\n...\\n...\\n"  # AC-1.1, AC-1.2

# US-2: Drop single blocks that fall and land
def test_drop_single_block():
    board = Board(3, 3)
    board.drop_block('A')
    assert str(board) == "...\\n.A.\\n...\\n"  # AC-2.2, AC-2.3

def test_block_falls_one_row_per_tick():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()
    assert str(board) == "...\\n.A.\\n...\\n"  # Block is still falling
    board.tick()
    assert str(board) == "...\\n...\\n.A.\\n"  # Block has landed

def test_block_lands_at_bottom():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # Falls to row 1
    board.tick()  # Falls to row 2
    board.tick()  # Should land now
    assert str(board) == "...\\n...\\n.A.\\n"  # Block has landed

def test_cannot_drop_block_if_already_falling():
    board = Board(3, 3)
    board.drop_block('A')
    assert board.drop_block('B') == "already falling"  # AC-2.6

def test_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # Falls to row 1
    board.tick()  # Lands
    board.drop_block('B')  # Now drop another block
    assert str(board) == "...\\n.B.\\n.A.\\n"  # AC-2.7

# US-3: Define pieces by their shape
def test_define_piece_shape():
    piece = Piece([".T.", "TTT", "..."])
    assert str(piece) == ".T.\\nTTT\\n..."  # AC-3.1

def test_rotating_piece_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    assert str(piece) == "...\\nXX.\\n..."  # AC-3.2

def test_rotating_piece_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    assert str(piece) == "...\\n.XX\\n..."  # AC-3.2

def test_stock_t_shape():
    piece = Piece([".T.", "TTT", "..."])
    assert str(piece) == ".T.\\nTTT\\n..."  # AC-3.3

# US-4: Play whole pieces on the board
def test_drop_piece_at_top():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    assert str(board) == "...T..\\n..TTT.\\n......"  # AC-4.1

def test_piece_lands_on_board():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.tick()  # Move down
    board.tick()  # Should land now
    assert str(board) == "...T..\\n..TTT.\\n......"  # Piece has landed

def test_piece_stops_on_landed_material():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.tick()  # Move down
    board.tick()  # Land
    board.drop_block('A')  # Drop a block
    assert str(board) == "...T..\\n..TTT.\\n...A.."  # AC-4.4

def test_piece_with_no_room_lands_immediately():
    board = Board(6, 3)
    piece = Piece(["TTT", ".T.", "..."])
    board.drop_piece(piece)
    assert str(board) == "TTT...\\n.T....\\n......"  # AC-4.7

def test_clipped_piece_at_right_edge():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_right()  # Move to the right edge
    board.steer_right()  # Should not move right
    assert str(board) == "...T..\\n..TTT.\\n......"  # AC-4.8

def test_clipped_piece_at_bottom_edge():
    board = Board(3, 3)
    piece = Piece(["TTT", "T..", "..."])
    board.drop_piece(piece)
    assert str(board) == "TTT\\nT..\\n..."  # AC-4.8

def test_multiple_drops():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # A falls to row 1
    board.drop_block('B')  # Attempt to drop B while A is falling
    assert board.drop_block('C') == "already falling"  # AC-4.5
    board.tick()  # A lands
    assert str(board) == "...\\n.B.\\n.A.\\n"  # B has landed on A

# US-5: Steer the falling piece
def test_steer_piece_left():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_left()  # Should move left
    assert str(board) == "..T...\\n..TTT.\\n......"  # AC-5.1

def test_steer_piece_right():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_right()  # Should move right
    assert str(board) == "...T..\\n..TTT.\\n......"  # AC-5.1

def test_cannot_steer_piece_out_of_bounds():
    board = Board(3, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.steer_left()  # Should be able to move left
    board.steer_left()  # Should not be able to move left
    assert str(board) == "...T..\\n..TTT.\\n......"  # AC-5.2

# US-6: Rotate the falling piece
def test_rotate_falling_piece():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.rotate_right()  # Rotate piece
    assert str(board) == "......\\n..TT..\\n...T.."  # AC-6.1

def test_rotation_abandoned_if_blocked():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.drop_block('A')  # Block below
    board.rotate_right()  # Should not rotate
    assert str(board) == "......\\n..TT..\\n...T.."  # AC-6.2

def test_rotate_single_block():
    board = Board(6, 3)
    board.drop_block('A')
    board.rotate_right()  # Should do nothing
    assert str(board) == "...\\n.A.\\n..."  # AC-6.3
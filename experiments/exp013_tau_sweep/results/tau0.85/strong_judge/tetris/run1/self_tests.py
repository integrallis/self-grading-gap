from solution import Board, Piece

def test_board_initialization():
    board = Board(3, 3)
    assert board.render() == "...\n...\n...\n"  # AC-1.1: Empty board with dots

def test_board_rendering():
    board = Board(4, 2)
    assert board.render() == "....\n....\n"  # AC-1.1: Empty 4x2 board with dots

def test_drop_single_block():
    board = Board(3, 3)
    board.drop_block('A')
    assert board.render() == ".A.\n...\n...\n"  # AC-2.3: Block 'A' at top middle

def test_drop_single_block_6_wide():
    board = Board(6, 4)
    board.drop_block('A')
    assert board.render() == "....A.\n......\n......\n......\n"  # Block 'A' at column 4 on a 6-wide board

def test_single_block_falls():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()
    assert board.render() == "...\n.A.\n...\n"  # Block 'A' at (1, 0)

    board.tick()
    assert board.render() == "...\n...\n.A.\n"  # Block 'A' at (2, 0)

def test_block_lands():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # (1, 0)
    board.tick()  # (2, 0)
    board.tick()  # Should land
    assert board.render() == "...\n...\n.A.\n"  # Block 'A' settled at (2, 0)

def test_block_stops_at_bottom():
    board = Board(3, 3)
    board.drop_block('A')
    for _ in range(3):
        board.tick()  # Move to bottom (2, 0)
    board.tick()  # Should stay at (2, 0)
    assert board.render() == "...\n...\n.A.\n"

def test_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop_block('A')  # A falls
    board.tick()  # (1, 0)
    board.tick()  # (2, 0)
    board.tick()  # Lands
    result = board.drop_block('B')  # Now drop block B
    assert result == "already falling"  # AC-2.6: Message when trying to drop while falling
    board.tick()  # Settle A
    assert board.render() == "...\n...\n.A.\n"  # Block 'A' settled at (2, 0)

def test_define_piece_shape():
    piece = Piece([".T.", "TTT", "..."])
    assert piece.render() == [".T.", "TTT", "..."]  # AC-3.1: Shape rendering

def test_rotate_piece_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    assert piece.render() == ["...", "XX.", "..."]  # AC-3.2: Right rotation

def test_rotate_piece_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    assert piece.render() == ["...", ".XX", "..."]  # AC-3.2: Left rotation

def test_drop_piece():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    assert board.render() == "....T.\n...TTT\n......\n......\n"  # AC-4.1: Piece at top middle

def test_piece_falls():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    board.tick()  # Move down
    assert board.render() == "......\n....T.\n...TTT\n......\n"  # Piece moves down

def test_piece_lands():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    for _ in range(3):  # Fall to bottom
        board.tick()  
    board.tick()  # Lands
    assert board.render() == "......\n......\n....T.\n...TTT\n"  # Piece settled

def test_piece_clips():
    piece = Piece(["..T.", "TTT", "..."])
    board = Board(6, 2)
    board.drop_piece(piece)
    assert board.render() == "...T.\n.TTT.\n"  # Piece settled at bottom

def test_immediate_landing():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 2)
    board.drop_piece(piece)
    assert board.render() == "...T.\n..TTT\n"  # Piece cannot fall, settles immediately

def test_steer_piece_left():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    board.tick()  # Move down
    board.steer_left()
    assert board.render() == "......\n..T...\n.TTT..\n......\n"  # Piece moved left

def test_steer_piece_right():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    board.tick()  # Move down
    board.steer_right()  # Should not move right beyond the edge
    assert board.render() == "......\n....T.\n...TTT\n......\n"  # Piece remains in original position

def test_rotate_piece():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    board.rotate_right()
    assert board.render() == "......\n...T..\n...TT.\n......\n"  # Piece rotated

def test_piece_lands_on_side_wall():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    for _ in range(2):  # Fall down
        board.tick()
    board.steer_left()  # Move to left wall
    board.tick()  # Should land
    assert board.render() == "......\n.T...\nTTT..\n......\n"  # Piece settled against left wall

def test_steer_left_boundary_refusal():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    for _ in range(2):  # Move down
        board.tick()
    board.steer_left()  # Move left
    board.steer_left()  # Attempt to move left again
    assert board.render() == "......\n...T..\n..TTT.\n......\n"  # Piece stays against left wall

def test_steer_right_boundary_refusal():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    for _ in range(2):  # Move down
        board.tick()
    board.steer_right()  # Move down
    board.steer_right()  # Attempt to move right again
    assert board.render() == "......\n......\n....T.\n...TTT\n"  # Piece stays against right wall

def test_block_blocked_by_landed_material():
    board = Board(3, 3)
    board.drop_block('A')  # Drop block A
    for _ in range(2):  # A lands
        board.tick()
    assert board.render() == "...\n...\n.A.\n"  # Block A settled
    result = board.drop_block('B')  # Now drop block B
    assert result == "already falling"  # AC-2.6: Message when trying to drop while falling

def test_steer_and_rotate_empty_board():
    board = Board(3, 3)
    board.steer_left()  # No falling piece, should change nothing
    board.steer_right()  # No falling piece, should change nothing
    assert board.render() == "...\n...\n...\n"  # Board unchanged

def test_drop_piece_while_block_falls():
    board = Board(6, 4)
    board.drop_block('A')  # Drop A
    result = board.drop_piece(Piece([".T.", "TTT", "..."]))  # Attempt to drop piece
    assert result == "already falling"  # AC-2.6: Message when trying to drop while falling

def test_drop_block_while_piece_falls():
    piece = Piece([".T.", "TTT", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)  # Drop piece
    board.tick()
    result = board.drop_block('A')  # Attempt to drop block
    assert result == "already falling"  # AC-2.6: Message when trying to drop while falling

def test_transparency_of_falling_piece():
    piece = Piece([".X.", "X.X", "..."])
    board = Board(6, 4)
    board.drop_piece(piece)
    board.tick()  # Move down
    assert board.render() == "......\n....X.\nX.X...\n......\n"  # Transparent cells show blocks behind

def test_right_edge_clipping():
    piece = Piece([".T.", "TT.", "T.."])  # Width 3 piece
    board = Board(6, 2)  # Width 6 board
    board.drop_piece(piece)
    assert board.render() == "...T.\n..TT.\n......\n"  # Right edge clipping

def test_bottom_edge_clipping():
    piece = Piece([".T.", "TTT", "T.."])  # Height 3 piece
    board = Board(6, 2)  # Height 2 board
    board.drop_piece(piece)
    assert board.render() == "...T.\n..TT.\n"  # Bottom edge clipping

def test_stock_t_shape():
    piece = Piece([".T.", "TTT", "..."])  # Define T shape
    assert piece.render() == [".T.", "TTT", "..."]  # AC-3.3: Stock T shape rendering
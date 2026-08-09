from solution import Board, Piece

# US-1: See the board
def test_empty_board_rendering():
    board = Board(3, 3)
    assert board.render() == '...\n...\n...\n'  # AC-1.1

def test_board_rendering_size():
    board = Board(3, 3)
    assert len(board.render().splitlines()) == 3  # AC-1.2

def test_empty_board_rendering_6x3():
    board = Board(6, 3)
    assert board.render() == '......\n......\n......\n'  # AC-1.1

# US-2: Drop single blocks that fall and land
def test_new_board_has_nothing_falling():
    board = Board(3, 3)
    assert board.render() == '...\n...\n...\n'  # AC-2.1

def test_drop_single_block():
    board = Board(3, 3)
    board.drop_block('X')
    assert board.render() == '...\n.X.\n...\n'  # AC-2.2

def test_drop_single_block_position():
    board = Board(3, 3)
    board.drop_block('X')
    assert board.render() == '...\n.X.\n...\n'  # AC-2.3

def test_falling_single_block_moves_down():
    board = Board(3, 3)
    board.drop_block('X')
    board.tick()  # Move down
    assert board.render() == '...\n.X.\n...\n'  # AC-2.4

def test_block_lands_at_bottom():
    board = Board(3, 3)
    board.drop_block('X')
    for _ in range(3):  # Move down until it lands
        board.tick()
    board.tick()  # Extra tick to check the block doesn't go through
    assert board.render() == '...\n...\n.X.\n'  # AC-2.5

def test_cannot_drop_block_when_already_falling():
    board = Board(3, 3)
    board.drop_block('X')
    result = board.drop_block('Y')
    assert result == "already falling"  # AC-2.6

def test_falling_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop_block('X')
    for _ in range(2):  # Move down once, then land
        board.tick()
    result = board.drop_block('Y')  # New block should not drop through
    assert result == "already falling"  # AC-2.7
    assert board.render() == '...\n.X.\n...\n'  # Check board remains the same after failed drop

def test_bottom_row_block_remains_falling():
    board = Board(3, 3)
    board.drop_block('X')
    for _ in range(2):  # Move down until it reaches the bottom
        board.tick()
    assert board.render() == '...\n...\n.X.\n'  # Should still be falling
    board.tick()  # Now it should stop
    assert board.render() == '...\n...\n.X.\n'  # AC-2.5

# US-3: Define pieces by their shape
def test_piece_shape_rendering():
    piece = Piece([".T.", "TTT", "..."])
    # Render is not specified, so we check the shape instead
    assert piece.shape == [".T.", "TTT", "..."]  # AC-3.1

def test_piece_rotation_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    assert piece.shape == ["...", ".XX", "..."]  # AC-3.2

def test_piece_rotation_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    assert piece.shape == ["...", "XX.", "..."]  # AC-3.2

def test_t_shape_rendering():
    piece = Piece([".T.", "TTT", "..."])
    # Render is not specified, so we check the shape instead
    assert piece.shape == [".T.", "TTT", "..."]  # AC-3.3

# US-4: Play whole pieces on the board
def test_drop_piece_on_board_6x3():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    assert board.render() == "....T.\n..TTT.\n......\n"  # AC-4.1

def test_drop_piece_on_board_7x3():
    board = Board(7, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    assert board.render() == "....T..\n...TTT.\n.......\n"  # AC-4.1

def test_falling_piece_moves_down():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()
    assert board.render() == "......\n....T.\n..TTT.\n"  # AC-4.2

def test_piece_lands():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    for _ in range(2):  # Move down until it lands
        board.tick()
    assert board.render() == "......\n....T.\n..TTT.\n"  # AC-4.3

def test_piece_stops_on_landed_material():
    board = Board(6, 3)
    board.drop_block('X')
    for _ in range(2):  # Drop the block
        board.tick()
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)  # New piece should settle above
    assert board.render() == "......\n....X.\n..TTT.\n"  # AC-4.4

def test_drop_blocks_and_pieces_successively():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.tick()  # Move piece down again
    board.drop_block('X')  # Drop block after piece has settled
    assert board.render() == "......\n....X.\n..TTT.\n"  # AC-4.5

def test_piece_with_no_room_lands_immediately():
    board = Board(3, 3)
    piece = Piece(["XXX", "XXX", "XXX"])  # Piece too big to fit
    board.drop_piece(piece)
    assert board.render() == "XXX\nXXX\nXXX\n"  # AC-4.7

def test_piece_clipping_out_of_bounds():
    board = Board(5, 3)
    piece = Piece(["XXXX", "XXXX", "XXXX"])  # Piece too wide
    board.drop_piece(piece)
    assert board.render() == ".....\n.....\n.....\n"  # AC-4.8

# US-5: Steer the falling piece
def test_steer_falling_piece_left():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.move_left()  # Steer left
    assert board.render() == "......\n..T...\n.TTT..\n"  # AC-5.1

def test_steer_falling_piece_right():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.move_right()  # Steer right
    assert board.render() == "......\n....T.\n...TTT\n"  # AC-5.1

def test_steer_falling_piece_beyond_boundary():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.move_left()  # Move left to "..T.."
    board.move_left()  # Move left to ".T..."
    board.move_left()  # Should not move left beyond boundary
    assert board.render() == "......\n..T...\n.TTT..\n"  # AC-5.2

def test_no_move_when_nothing_falling():
    board = Board(6, 3)
    board.move_left()  # Nothing to move
    assert board.render() == "......\n......\n......\n"  # AC-5.4

def test_no_move_or_rotate_when_nothing_falling():
    board = Board(6, 3)
    board.move_left()  # Nothing to move
    board.rotate_right()  # Nothing to rotate
    assert board.render() == "......\n......\n......\n"  # AC-5.4

# US-6: Rotate the falling piece
def test_rotate_falling_piece_clockwise():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.rotate_right()  # Rotate in place
    assert board.render() == "......\n...T..\nTT...\n"  # AC-6.1

def test_rotate_falling_piece_counterclockwise():
    board = Board(6, 3)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.rotate_left()  # Rotate in place
    assert board.render() == "......\n..T...\n...TT\n"  # AC-6.1

def test_rotate_piece_if_fit():
    board = Board(7, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move piece down
    board.move_right()  # Steer right
    board.rotate_right()  # Rotate piece
    assert board.render() == "......\n......\n...T..\nTT...\n"  # AC-6.2

def test_abort_rotation_if_blocked():
    board = Board(6, 3)
    board.drop_block('X')  # Block below
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.rotate_right()  # Attempt to rotate but blocked
    assert board.render() == "......\n...T..\nTT...\n"  # AC-6.2

def test_rotating_single_block_has_no_effect():
    board = Board(6, 3)
    board.drop_block('X')
    board.rotate_right()  # Should do nothing
    assert board.render() == '...\n.X.\n...\n'  # AC-6.3

def test_falling_single_block_can_move_left_and_right():
    board = Board(6, 3)
    board.drop_block('X')
    board.tick()  # Move down
    board.move_left()  # Steer left
    assert board.render() == '...\n.X.\n...\n'  # Block can move left
    board.move_right()  # Steer right
    assert board.render() == '...\n.X.\n...\n'  # Block should move back to original position
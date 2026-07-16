from solution import World

def test_empty_world_population():
    world = World()
    assert world.population() == 0  # An empty world has no live cells.

def test_empty_world_live_cells():
    world = World()
    assert world.live_cells() == set()  # An empty world has an empty set of live cells.

def test_advance_generation_empty_world():
    world = World()
    new_world = world.advance()
    assert new_world.live_cells() == set()  # Advancing an empty world should still yield an empty world.

def test_live_cell_with_few_neighbors_dies():
    world = World({(0, 0)})  # One live cell
    new_world = world.advance()
    assert new_world.live_cells() == set()  # Dies of underpopulation (fewer than 2 neighbors).

def test_live_cell_with_two_neighbors_survives():
    world = World({(0, 0), (0, 1), (1, 0)})  # One live cell with two live neighbors
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0)}  # Survives.

def test_live_cell_with_three_neighbors_survives():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # One live cell with three live neighbors
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Survives.

def test_live_cell_with_four_neighbors_dies():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)})  # One live cell with four live neighbors
    new_world = world.advance()
    assert new_world.live_cells() == {(1, 0), (1, 1)}  # Dies of overpopulation.

def test_dead_cell_with_three_neighbors_becomes_alive():
    world = World({(0, 0), (0, 1), (1, 0)})  # Three live neighbors surrounding (1, 1)
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0), (0, 1), (1, 0), (1, 1)}  # (1, 1) becomes alive.

def test_dead_cell_with_two_neighbors_stays_dead():
    world = World({(0, 0), (0, 1)})  # Two live neighbors around (1, 1)
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0), (0, 1)}  # (1, 1) stays dead.

def test_still_life_block():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block shape
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Block remains unchanged.

def test_still_life_beehive():
    world = World({(0, 1), (1, 0), (1, 2), (2, 1)})  # Beehive shape
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 1), (1, 0), (1, 2), (2, 1)}  # Beehive remains unchanged.

def test_blinker():
    world = World({(0, 1), (1, 1), (2, 1)})  # Horizontal blinker
    new_world = world.advance()  # To vertical
    assert new_world.live_cells() == {(1, 0), (1, 1), (1, 2)}  # Blinkers should turn vertically.
    new_world = new_world.advance()  # Back to horizontal
    assert new_world.live_cells() == {(0, 1), (1, 1), (2, 1)}  # Blinkers should return to original shape.

def test_toad():
    world = World({(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)})  # Toad shape
    new_world = world.advance()  # Changes shape
    assert new_world.live_cells() == {(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)}  # Toad changes shape.
    new_world = new_world.advance()  # Back to original shape
    assert new_world.live_cells() == {(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}  # Returns to original.

def test_glider():
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})  # Glider shape
    for _ in range(4):
        world = world.advance()
    assert world.live_cells() == {(1, 2), (2, 1), (2, 2), (3, 1), (3, 2)}  # Glider moves diagonally.

def test_text_representation():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block shape
    assert world.to_text() == ['**', '**']  # Text representation matches the shape.

def test_window_rendering():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block shape
    assert world.render(2, 2) == ['**', '**']  # Render a 2x2 window.

def test_render_empty_world():
    world = World()
    assert world.render(5, 5) == ['.....', '.....', '.....', '.....', '.....']  # Empty world renders as all dead.

def test_equal_worlds():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (0, 0)})
    assert world1 == world2  # Different order but same live cells should be equal.

def test_unequal_worlds():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(0, 0), (1, 2)})
    assert world1 != world2  # Different live cells should not be equal.

def test_hashing():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (0, 0)})
    assert hash(world1) == hash(world2)  # Same live cells should have the same hash.

def test_different_hashes():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(0, 1), (1, 1)})
    assert hash(world1) != hash(world2)  # Different live cells should have different hashes.

def test_live_neighbours_count():
    world = World({(0, 0), (0, 1), (1, 0)})
    assert world.live_neighbours_count((0, 0)) == 2  # Two live neighbors.
    assert world.live_neighbours_count((0, 1)) == 1  # One live neighbor.
    assert world.live_neighbours_count((1, 1)) == 3  # Three live neighbors.
    assert world.live_neighbours_count((2, 2)) == 0  # No live neighbors far away.
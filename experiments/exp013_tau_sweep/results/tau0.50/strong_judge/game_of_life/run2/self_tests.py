from solution import World

def test_empty_world_population():
    world = World()
    assert world.population() == 0  # AC-4.1: An empty world has a population of zero.

def test_empty_world_live_cells():
    world = World()
    assert world.live_cells() == set()  # AC-4.1: An empty world has an empty set of live cells.

def test_advance_empty_world():
    world = World()
    new_world = world.advance()
    assert new_world.live_cells() == set()  # AC-4.2: Advancing an empty world returns another empty world.

def test_single_live_cell_underpopulation():
    world = World({(0, 0)})  # A single live cell
    new_world = world.advance()
    assert new_world.live_cells() == set()  # AC-1.1: Underpopulation causes the cell to die.

def test_single_live_cell_with_two_neighbours():
    world = World({(0, 0), (1, 0)})  # Two live neighbours for a dead cell
    new_world = world.advance()
    assert new_world.live_cells() == set()  # AC-1.4: Dead cell remains dead with two neighbours.

def test_single_live_cell_with_three_neighbours():
    world = World({(0, 0), (1, 0), (0, 1), (1, 1)})  # A cell with three live neighbours
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0), (1, 0), (0, 1), (1, 1)}  # AC-1.2: Survives with three neighbours.

def test_single_live_cell_overpopulation():
    world = World({(0, 0), (1, 0), (0, 1), (1, 1), (1, -1)})  # More than three neighbours
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 1), (1, 1), (1, -1), (0, -1), (2, 0)}  # AC-1.3: Overpopulation causes the cell to die.

def test_dead_cell_with_three_neighbours():
    world = World({(0, 0), (1, 0), (0, 1)})  # Three live neighbours for a dead cell
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 0), (1, 0), (0, 1), (1, 1)}  # AC-1.4: Dead cell becomes alive with three neighbours.

def test_still_life_block():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block pattern
    new_world = world.advance()
    assert new_world.live_cells() == world.live_cells()  # AC-2.1: Block reproduces itself.
    new_world = new_world.advance()
    assert new_world.live_cells() == world.live_cells()  # Verify it remains unchanged after another advance.

def test_still_life_beehive():
    world = World({(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)})  # Canonical beehive pattern
    new_world = world.advance()
    assert new_world.live_cells() == world.live_cells()  # AC-2.1: Beehive reproduces itself.
    new_world = new_world.advance()
    assert new_world.live_cells() == world.live_cells()  # Verify it remains unchanged after another advance.

def test_blinker():
    world = World({(0, 0), (0, 1), (0, 2)})  # Blinker pattern
    new_world = world.advance()
    assert new_world.live_cells() == {(0, 1), (1, 1), (2, 1)}  # AC-2.2: Blinker turns to vertical.
    new_world = new_world.advance()
    assert new_world.live_cells() == {(0, 0), (0, 1), (0, 2)}  # Returns to original shape.

def test_toad():
    world = World({(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (1, 3)})  # Toad pattern
    new_world = world.advance()
    assert new_world.live_cells() == {(-1, 1), (0, 0), (0, 3), (1, 0), (1, 3), (2, 2)}  # AC-2.3: Toad changes shape.
    new_world = new_world.advance()
    assert new_world.live_cells() == world.live_cells()  # Returns to original shape.

def test_glider():
    world = World({(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)})  # Glider pattern
    for _ in range(4):
        new_world = world.advance()
        world = new_world
    assert world.live_cells() == {(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1)}  # AC-2.4: Glider moves diagonally.

def test_world_from_text():
    text = ["*..", "***", "..."]
    world = World.from_text(text)
    assert world.live_cells() == {(0, 0), (1, 0), (1, 1), (1, 2)}  # AC-3.1: World built from text.

def test_render_world_to_text():
    world = World({(0, 0), (1, 0), (1, 1), (1, 2)})  # Example world
    text = world.to_text(3, 3)
    assert text == ["*..", "***", "..."]  # AC-3.2: Rendered back to text.

def test_render_pattern_back_to_text():
    text = ["*..", "***", "..."]
    world = World.from_text(text)
    assert world.to_text(3, 3) == text  # AC-3.3: Renders back to original text.

def test_world_equality():
    world1 = World({(0, 0), (1, 0)})
    world2 = World({(1, 0), (0, 0)})
    assert world1 == world2  # AC-4.4: Two worlds with the same cells are equal.

def test_world_hashing():
    world1 = World({(0, 0), (1, 0)})
    world2 = World({(1, 0), (0, 0)})
    assert hash(world1) == hash(world2)  # AC-4.4: Hashes are the same for equal worlds.
    world3 = World({(0, 1)})
    world4 = World({(1, 1)})
    assert len({hash(world1), hash(world2), hash(world3), hash(world4)}) > 1  # AC-4.5: Different worlds have different hashes.

def test_live_neighbours():
    world = World({(0, 0), (1, 0), (0, 1)})
    assert world.count_live_neighbours((0, 0)) == 2  # AC-4.6: Cell has two live neighbours.
    assert world.count_live_neighbours((0, 1)) == 1  # Cell has one live neighbour.
    assert world.count_live_neighbours((2, 2)) == 0  # Far from any live cells.

def test_neighbour_count_adjacent_dead():
    world = World({(0, 0), (1, 0), (0, 1)})  # L-triomino
    assert world.count_live_neighbours((1, 1)) == 3  # AC-4.6: Dead cell with three live neighbours.

def test_advance_nonempty_oscillator():
    world = World({(0, 0), (0, 1), (0, 2)})  # Blinker pattern
    new_world = world.advance()
    assert new_world.live_cells() != world.live_cells()  # New world must be different.
    assert world.live_cells() == {(0, 0), (0, 1), (0, 2)}  # Original remains unchanged.

def test_arbitrarily_distant_coordinate():
    world = World({(0, 0)})  # A world with one live cell
    assert world.count_live_neighbours((100, 100)) == 0  # AC-4.3: Far from any live cells.
    assert world.count_live_neighbours((100, 100)) == 0  # Distant cell reports dead.
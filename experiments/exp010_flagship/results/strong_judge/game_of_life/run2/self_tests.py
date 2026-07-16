from solution import World

def test_evolve_underpopulation():
    # A live cell with fewer than two live neighbours dies of underpopulation.
    world = World({(0, 0)})  # One live cell at (0, 0)
    next_world = world.advance()  # Advance to next generation
    assert next_world.live_cells == set()  # Expected: no live cells

def test_evolve_survival():
    # A live cell with two live neighbours survives.
    world = World({(0, 1), (1, 0), (1, 1)})  # (0, 1) has three live neighbours
    next_world = world.advance()  # Advance to next generation
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Expected: (0, 0) is born

def test_evolve_overpopulation():
    # A live cell with more than three live neighbours dies of overpopulation.
    world = World({(0, 0), (0, 1), (0, 2), (1, 1), (1, 0)})  # More than 3 neighbours for (0, 1)
    next_world = world.advance()  # Advance to next generation
    assert next_world.live_cells == {(-1, 1), (0, 0), (0, 2), (1, 0), (1, 2)}  # Expected: (0, 1) dies

def test_evolve_reproduction():
    # A dead cell with exactly three live neighbours becomes alive.
    world = World({(0, 0), (0, 1), (1, 0)})  # Three live neighbours for (1, 1)
    next_world = world.advance()  # Advance to next generation
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Expected: (1, 1) is born

def test_evolve_empty_world():
    # An empty world stays empty: nothing is ever born from no live cells.
    world = World(set())  # No live cells
    next_world = world.advance()  # Advance to next generation
    assert next_world.live_cells == set()  # Expected: still no live cells

def test_evolve_neighbourhood():
    # A cell's neighbourhood is exactly the eight surrounding cells.
    world = World({(0, 0)})  # One live cell
    assert world.count_live_neighbours((0, 0)) == 0  # Expected: 0 neighbours
    assert world.count_live_neighbours((0, 1)) == 1  # Expected: 1 neighbour
    assert world.count_live_neighbours((1, 0)) == 1  # Expected: 1 neighbour
    assert world.count_live_neighbours((1, 1)) == 1  # Expected: 1 neighbour
    assert world.count_live_neighbours((-1, -1)) == 1  # Expected: 1 neighbour
    assert world.count_live_neighbours((-1, 0)) == 1  # Expected: 1 neighbour
    assert world.count_live_neighbours((0, -1)) == 1  # Expected: 1 neighbour
    assert world.count_live_neighbours((-1, 1)) == 1  # Expected: 1 neighbour

def test_still_lifes():
    # Still lifes reproduce themselves exactly, generation after generation.
    world_block = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block
    next_world_block = world_block.advance()  # Advance to next generation
    assert next_world_block.live_cells == world_block.live_cells  # Expected: same cells

    world_beehive = World({(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)})  # Beehive
    next_world_beehive = world_beehive.advance()  # Advance to next generation
    assert next_world_beehive.live_cells == world_beehive.live_cells  # Expected: same cells

def test_blinker():
    # The blinker alternates between vertical and horizontal.
    world = World({(0, 0), (1, 0), (2, 0)})  # Horizontal blinker
    next_world = world.advance()  # First evolution: vertical
    assert next_world.live_cells == {(1, -1), (1, 0), (1, 1)}  # Expected: vertical blinker
    next_next_world = next_world.advance()  # Second evolution: back to horizontal
    assert next_next_world.live_cells == world.live_cells  # Expected: same as original

def test_toad():
    # The toad changes shape after one generation and returns to its original shape after two.
    world = World({(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)})  # Canonical six-cell toad
    next_world = world.advance()  # First evolution
    assert next_world.live_cells == {(-1, 2), (0, 0), (0, 3), (1, 0), (1, 3), (2, 1)}  # Expected: first change
    next_next_world = next_world.advance()  # Second evolution: back to original
    assert next_next_world.live_cells == world.live_cells  # Expected: same as original

def test_glider():
    # The glider translates itself diagonally by one cell every four generations.
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})  # Initial glider
    for _ in range(4):  # Advance four generations
        world = world.advance()
    assert world.live_cells == {(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)}  # Expected: glider moved

def test_build_world_from_text():
    # A world can be built from rows of text.
    text = ["*..", ".*.", "..*"]
    world = World.from_text(text)  # Build world from text
    assert world.live_cells == {(0, 0), (1, 1), (2, 2)}  # Expected live cells based on text

def test_render_world_as_text():
    # A rectangular window of the plane renders as text.
    world = World({(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)})  # Block and a dead cell
    rendered = world.render(3, 2)  # Render a 3x2 window
    expected_render = ["**.", "**."]  # Expected text output
    assert rendered == expected_render  # Expected: match rendered output

def test_pattern_renders_back_to_exact_rows():
    # A pattern built from rows of text renders back to exactly those rows.
    text = ["*.*", ".*.", "*.*"]
    world = World.from_text(text)  # Build world from text
    assert world.render(3, 3) == text  # Expected: render back to original text

def test_empty_world_population():
    # An empty world has a population of zero.
    world = World(set())
    assert len(world.live_cells) == 0  # Expected: population is 0

def test_advance_returns_new_world():
    # Advancing a generation returns a new world and leaves the original untouched.
    world = World({(0, 0)})
    next_world = world.advance()
    assert next_world.live_cells != world.live_cells  # Expected: next world is not the same
    assert world.live_cells == {(0, 0)}  # Expected: original world remains unchanged

def test_far_away_coordinates_dead():
    # Arbitrarily distant coordinates report a dead cell.
    world = World({(0, 0)})
    assert world.count_live_neighbours((100, 100)) == 0  # Expected: far away cell is dead
    assert (100, 100) not in world.live_cells  # Expected: (100, 100) is not alive

def test_world_equality_and_hashing():
    # Two worlds with the same live cells are equal and hash alike.
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (0, 0)})
    assert world1 == world2  # Expected: worlds are equal
    assert hash(world1) == hash(world2)  # Expected: hashes are the same

    world3 = World({(0, 0)})
    assert world1 != world3  # Expected: worlds are not equal
from solution import World

def test_evolve_underpopulation():
    # A live cell with fewer than two live neighbours dies of underpopulation.
    world = World({(0, 0)})  # Cell (0, 0) is alive
    next_world = world.evolve()
    assert next_world.live_cells == set()  # The cell dies

def test_evolve_survival():
    # A live cell with two or three live neighbours survives into the next generation.
    world = World({(0, 0), (0, 1), (1, 1)})  # Two cells (0,0), (0,1) have 2 neighbours, survive
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 1)}  # Survives

    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block, all survive
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Survives

def test_evolve_overpopulation():
    # A live cell with more than three live neighbours dies of overpopulation.
    world = World({(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)})  # Cell (0, 1) has 5 neighbours
    next_world = world.evolve()
    assert next_world.live_cells == {(-1, 1), (0, 0), (0, 2), (1, 0), (1, 2), (2, 1)}  # Corrected expectation

def test_evolve_reproduction():
    # A dead cell with exactly three live neighbours becomes alive.
    world = World({(0, 0), (0, 1), (1, 0)})  # Cell (1, 1) will become alive
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Cell (1,1) is now alive

def test_evolve_empty_world():
    # An empty world stays empty.
    world = World(set())
    next_world = world.evolve()
    assert next_world.live_cells == set()  # Still empty

def test_evolve_neighbourhood():
    # A cell's neighbourhood is the eight surrounding cells
    world = World({(0, 0)})  # Cell (0, 0) is alive
    assert world.neighbours((0, 0)) == {(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)}

def test_still_life_block():
    # The block pattern reproduces itself exactly.
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Remains the same

def test_still_life_beehive():
    # The beehive pattern reproduces itself exactly.
    world = World({(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)})  # Canonical beehive
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)}  # Remains the same

def test_blinker():
    # The blinker alternates between vertical and horizontal.
    world = World({(0, 0), (0, 1), (0, 2)})
    next_world = world.evolve()
    assert next_world.live_cells == {(-1, 1), (0, 1), (1, 1)}  # Blinker becomes vertical
    next_next_world = next_world.evolve()
    assert next_next_world.live_cells == {(0, 0), (0, 1), (0, 2)}  # Returns to original

def test_toad():
    # The toad changes shape after one generation and returns to its original shape after two.
    world = World({(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (1, 3)})
    next_world = world.evolve()
    assert next_world.live_cells == {(-1, 1), (0, 0), (0, 3), (1, 0), (1, 3), (2, 2)}  # Changes shape
    next_next_world = next_world.evolve()
    assert next_next_world.live_cells == {(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (1, 3)}  # Returns to original

def test_glider():
    # The glider translates itself diagonally by one cell every four generations.
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})
    generations = [world]
    for _ in range(4):
        generations.append(generations[-1].evolve())
    assert generations[0].live_cells == {(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)}  # Initial state
    assert generations[1].live_cells == {(1, 0), (1, 2), (2, 1), (2, 2), (3, 1)}  # After 1 generation
    assert generations[2].live_cells == {(1, 2), (2, 0), (2, 2), (3, 1), (3, 2)}  # After 2 generations
    assert generations[3].live_cells == {(1, 1), (2, 2), (2, 3), (3, 1), (3, 2)}  # After 3 generations
    assert generations[4].live_cells == {(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)}  # After 4 generations

def test_world_from_text():
    # A world can be built from rows of text.
    text = ["*..", "...", ".*."]
    world = World.from_text(text)
    assert world.live_cells == {(0, 0), (2, 1)}  # Cells created from text

def test_render_world():
    # A rectangular window of the plane renders as text.
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})
    rendered = world.render(2, 2)
    assert rendered == ["**", "**"]  # Correct rendering

def test_pattern_rendering():
    # A pattern built from rows of text renders back to exactly those rows.
    text = ["*..", "*.."]
    world = World.from_text(text)
    assert world.render(3, 2) == text  # Rendering matches original text

def test_world_population():
    # A world created with no cells has a population of zero and an empty live-cell set.
    world = World(set())
    assert len(world.live_cells) == 0  # Population is zero
    assert world.live_cells == set()  # Empty set of live cells

def test_hashing_same_worlds():
    # Two worlds with the same live cells are equal and hash alike.
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (0, 0)})
    assert world1 == world2  # They are equal
    assert hash(world1) == hash(world2)  # Their hashes are the same

def test_hashing_different_worlds():
    # Distinct worlds do not all collide on one hash.
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (2, 2)})
    assert world1 != world2  # They are not equal
    assert hash(world1) != hash(world2)  # Their hashes are different

def test_neighbour_count():
    # The number of live neighbours can be queried for any coordinate.
    world = World({(0, 0), (0, 1), (1, 0)})
    assert world.count_neighbours((0, 0)) == 1  # One neighbour
    assert world.count_neighbours((0, 1)) == 1  # One neighbour
    assert world.count_neighbours((1, 1)) == 2  # Two neighbours
    assert world.count_neighbours((2, 2)) == 0  # No neighbours far away

def test_evolve_reproduction_no_birth():
    # A dead cell with exactly two live neighbours remains dead.
    world = World({(0, 0), (0, 1)})  # Cell (1, 1) has only 2 neighbours
    next_world = world.evolve()
    assert next_world.live_cells == set()  # All cells die due to underpopulation

def test_evolve_returns_new_world():
    # Evolve returns a distinct world object and leaves the original unchanged.
    world = World({(0, 0)})
    next_world = world.evolve()
    assert next_world is not world  # Different objects
    assert world.live_cells == {(0, 0)}  # Original unchanged

def test_evolve_far_away_coordinate_is_dead():
    # A coordinate far from all live cells is dead.
    world = World({(0, 0)})
    assert world.count_neighbours((1000, 1000)) == 0  # Coordinate far away is dead
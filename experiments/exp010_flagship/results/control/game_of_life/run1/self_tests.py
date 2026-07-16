from solution import World

def test_evolve_world():
    # A live cell with fewer than two live neighbours dies of underpopulation.
    world = World({(0, 0)})
    next_world = world.evolve()
    assert next_world.live_cells == set()  # Expected: no live cells

    # A live cell with two live neighbours survives into the next generation.
    world = World({(0, 0), (0, 1), (1, 0)})
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0)}  # Expected: same cells

    # A live cell with more than three live neighbours dies of overpopulation.
    world = World({(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)})
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 1), (1, 0), (1, 1), (1, 2)}  # Expected: (0,0) dies

    # A dead cell with exactly three live neighbours becomes alive.
    world = World({(0, 0), (0, 1), (1, 0)})
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Expected: (1,1) comes to life

    # An empty world stays empty.
    world = World(set())
    next_world = world.evolve()
    assert next_world.live_cells == set()  # Expected: no live cells

def test_still_lifes():
    # The two-by-two block reproduces itself exactly.
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})
    next_world = world.evolve()
    assert next_world.live_cells == world.live_cells  # Expected: same cells

    # The beehive reproduces itself exactly.
    world = World({(0, 1), (1, 0), (1, 2), (2, 1), (2, 2), (1, 1)})
    next_world = world.evolve()
    assert next_world.live_cells == world.live_cells  # Expected: same cells

def test_blinker():
    # The blinker alternates between vertical and horizontal.
    world = World({(0, 0), (0, 1), (0, 2)})
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 1), (1, 1), (2, 1)}  # Expected: vertical blinker
    next_world = next_world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (0, 2)}  # Expected: back to original

def test_toad():
    # The toad changes shape after one generation and returns to its original shape after two.
    world = World({(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)})
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)}  # Expected: new shape
    next_world = next_world.evolve()
    assert next_world.live_cells == world.live_cells  # Expected: back to original

def test_glider():
    # The glider translates itself diagonally by one cell every four generations.
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})
    for _ in range(4):
        world = world.evolve()
    assert world.live_cells == {(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)}  # Expected: translated glider

def test_world_from_text():
    # A world can be built from rows of text.
    world = World.from_text([".*.", "***", "..."])
    assert world.live_cells == {(0, 1), (1, 0), (1, 1), (1, 2)}  # Expected: live cells at (0,1), (1,0), (1,1), (1,2)

def test_render_window():
    # A rectangular window of the plane renders as text.
    world = World({(0, 0), (1, 1)})
    rendered = world.render_window(3, 3)
    expected_render = " *.\n.*.\n...\n"  # Expected: 3x3 window
    assert rendered == expected_render

def test_immutable_world():
    # Advancing a generation returns a new world and leaves the original world untouched.
    world = World({(0, 0)})
    next_world = world.evolve()
    assert next_world.live_cells != world.live_cells  # Expected: different world
    assert world.live_cells == {(0, 0)}  # Expected: original world unchanged

def test_equal_worlds():
    # Two worlds with the same live cells are equal.
    world1 = World({(0, 0), (0, 1)})
    world2 = World({(0, 1), (0, 0)})
    assert world1 == world2  # Expected: worlds are equal

def test_hash_worlds():
    # Hashing depends on the set of live cells.
    world1 = World({(0, 0), (0, 1)})
    world2 = World({(0, 1), (0, 0)})
    assert hash(world1) == hash(world2)  # Expected: same hash
    world3 = World({(1, 0), (1, 1)})
    assert hash(world1) != hash(world3)  # Expected: different hash

def test_live_neighbours_count():
    # The number of live neighbours can be queried for any coordinate.
    world = World({(0, 0), (0, 1), (1, 0)})
    count = world.live_neighbours_count((0, 0))  # Expected: 1 live neighbour
    assert count == 1
    count = world.live_neighbours_count((1, 1))  # Expected: 3 live neighbours
    assert count == 3
    count = world.live_neighbours_count((10, 10))  # Expected: 0 live neighbours (far away)
    assert count == 0
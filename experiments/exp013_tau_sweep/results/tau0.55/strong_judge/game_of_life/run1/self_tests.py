from solution import World

def test_evolve_underpopulation():
    # A live cell with fewer than two live neighbours dies of underpopulation.
    initial = World({(0, 0)})  # One live cell
    next_gen = initial.advance()
    expected = World(set())  # The cell dies, resulting in an empty world.
    assert next_gen == expected

def test_evolve_one_neighbour():
    # A live cell with exactly one live neighbour dies of underpopulation.
    initial = World({(0, 0), (1, 0)})  # Cell (0,0) has one live neighbour (1,0).
    next_gen = initial.advance()
    expected = World(set())  # The cell dies, resulting in an empty world.
    assert next_gen == expected

def test_evolve_survival():
    # A live cell with two or three live neighbours survives into the next generation.
    initial = World({(0, 0), (0, 1), (1, 0)})  # Cell (0,0) has two live neighbours.
    next_gen = initial.advance()
    expected = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Cell (1,1) is born from reproduction.
    assert next_gen == expected

def test_evolve_overpopulation():
    # A live cell with more than three live neighbours dies of overpopulation.
    initial = World({(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)})  # Cell (0,0) has five live neighbours.
    next_gen = initial.advance()
    expected = World({(0, 0), (0, 2), (1, 0), (1, 2), (-1, 1), (2, 1)})  # Adjusted for births and deaths.
    assert next_gen == expected

def test_evolve_reproduction():
    # A dead cell with exactly three live neighbours becomes alive.
    initial = World({(0, 0), (0, 1), (1, 0)})  # Cell (1, 1) has three live neighbours.
    next_gen = initial.advance()
    expected = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Cell (1,1) comes to life.
    assert next_gen == expected

def test_evolve_empty_world():
    # An empty world stays empty; nothing is ever born from no live cells.
    initial = World(set())
    next_gen = initial.advance()
    expected = World(set())  # Still empty.
    assert next_gen == expected

def test_neighbourhood_count():
    # The number of live neighbours can be queried for any coordinate.
    initial = World({(0, 0), (0, 1), (1, 0)})
    assert initial.live_neighbours((0, 0)) == 2  # (0,0) has two live neighbours.
    assert initial.live_neighbours((1, 1)) == 3  # (1,1) has three live neighbours.
    assert initial.live_neighbours((2, 2)) == 0  # (2,2) is far away and dead.
    assert initial.live_neighbours((1000, 1000)) == 0  # Far away coordinate should be dead.
    assert initial.live_neighbours((-1000, -1000)) == 0  # Far away coordinate should be dead.

def test_still_life_block():
    # The two-by-two block reproduces itself exactly, generation after generation.
    initial = World({(0, 0), (0, 1), (1, 0), (1, 1)})
    next_gen = initial.advance()
    expected = World({(0, 0), (0, 1), (1, 0), (1, 1)})
    assert next_gen == expected

def test_still_life_beehive():
    # The beehive reproduces itself exactly, generation after generation.
    initial = World({(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)})
    next_gen = initial.advance()
    expected = World({(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)})
    assert next_gen == expected

def test_blinker():
    # The blinker alternates between vertical and horizontal.
    initial = World({(0, 1), (1, 1), (2, 1)})  # Horizontal blinker
    next_gen = initial.advance()  # Becomes vertical
    expected = World({(1, 0), (1, 1), (1, 2)})
    assert next_gen == expected

    next_gen = next_gen.advance()  # Returns to horizontal
    expected = World({(0, 1), (1, 1), (2, 1)})
    assert next_gen == expected

def test_toad():
    # The toad changes shape after one generation and returns to its original shape after two.
    initial = World({(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)})  # Canonical six-cell toad
    next_gen = initial.advance()  # One generation
    expected = World({(2, -1), (0, 0), (3, 0), (0, 1), (3, 1), (1, 2)})
    assert next_gen == expected

    next_gen = next_gen.advance()  # Returns to original
    expected = World({(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)})
    assert next_gen == expected

def test_glider():
    # The glider translates itself diagonally by one cell every four generations.
    initial = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})
    for _ in range(4):
        initial = initial.advance()
    expected = World({(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)})  # Glider moves down-right
    assert initial == expected

def test_world_population_and_live_cells():
    # An empty world exposes population zero and an empty live-cell set.
    initial = World(set())
    assert initial.population() == 0  # Population should be zero
    assert initial.live_cells() == set()  # Live cells should be an empty set

def test_world_immutable():
    # Advancing returns a distinct world object and does not change the original live cells.
    initial = World({(0, 0), (0, 1)})
    next_gen = initial.advance()
    assert next_gen is not initial  # They should not be the same object
    assert initial.live_cells() == {(0, 0), (0, 1)}  # Original should remain unchanged

def test_render_world_from_text():
    # A world can be built from rows of text in which "*" marks a live cell and "." a dead one.
    text = [
        ".*.",
        "***",
        ".*."
    ]
    expected = World({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)})  # Live cells from text
    initial = World.from_text(text)
    assert initial == expected

def test_render_window():
    # A rectangular window of the plane, anchored at the origin with a given width and height, renders as text.
    initial = World({(1, 1), (1, 2), (2, 2)})
    rendered = initial.render_window(3, 3)
    expected_render = [
        "...",
        "..*",
        ".*.",
    ]
    assert rendered == expected_render

def test_round_trip_text():
    # A pattern built from rows of text renders back to exactly those rows.
    text = [
        ".*.",
        "***",
        ".*."
    ]
    initial = World.from_text(text)
    assert initial.render_text() == text  # Should render back to the original text

def test_world_equality_and_hash():
    # Two worlds with the same live cells are equal and hash alike, regardless of the order.
    world1 = World({(0, 0), (1, 1), (2, 2)})
    world2 = World({(2, 2), (1, 1), (0, 0)})
    assert world1 == world2  # They should be equal
    assert hash(world1) == hash(world2)  # They should have the same hash

def test_world_distinct_hash():
    # Distinct worlds do not all collide on one hash.
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(2, 2), (3, 3)})
    assert world1 != world2  # They should not be equal
    assert hash(world1) != hash(world2)  # They should have different hashes

def test_far_away_coordinate():
    # A coordinate arbitrarily far from the pattern should be dead.
    initial = World({(0, 0)})
    assert initial.live_neighbours((1000, 1000)) == 0  # Far away coordinate should be dead
    assert not (1000, 1000) in initial.live_cells()  # The coordinate should not be in the live cell set
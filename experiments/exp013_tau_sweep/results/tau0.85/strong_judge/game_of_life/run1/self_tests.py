from solution import World

def test_evolve_underpopulation():
    # A live cell with fewer than two live neighbours dies of underpopulation
    world = World({(0, 0)})  # 1 live cell
    next_world = world.evolve()
    assert next_world.live_cells == set()  # Expected: no live cells

def test_evolve_survival_two_neighbours():
    # A live cell with two live neighbours survives into the next generation
    world = World({(0, 0), (0, 1), (1, 0)})  # (0, 0) has 2 neighbours
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Expected: (0, 0) survives and (1, 1) is born

def test_evolve_survival_three_neighbours():
    # A live cell with three live neighbours survives into the next generation
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # (0, 0) has 3 neighbours
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Expected: (0, 0) survives

def test_evolve_overpopulation():
    # A live cell with more than three live neighbours dies of overpopulation
    world = World({(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)})  # 1 live cell with 5 neighbours
    next_world = world.evolve()
    assert next_world.live_cells == {(-1, 1), (0, 0), (0, 2), (1, 0), (1, 2), (2, 1)}  # Expected: surviving cells

def test_evolve_reproduction():
    # A dead cell with exactly three live neighbours becomes alive
    world = World({(0, 0), (0, 1), (1, 0)})  # Dead cell at (1, 1) has exactly 3 live neighbours
    next_world = world.evolve()
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Expected: (1, 1) becomes alive

def test_evolve_reproduction_boundary():
    # A dead cell with exactly two live neighbours remains dead
    world = World({(0, 0), (0, 1)})  # Dead cell at (1, 0) has exactly 2 live neighbours
    next_world = world.evolve()
    assert next_world.live_cells == set()  # Expected: no cells alive

def test_evolve_empty_world():
    # An empty world stays empty
    world = World(set())  # No live cells
    next_world = world.evolve()
    assert next_world.live_cells == set()  # Expected: still no live cells

def test_evolve_neighbourhood():
    # Ensure the neighbourhood is exactly the eight surrounding cells
    world = World({(0, 0)})  # Test cell
    assert world.get_neighbour_count((0, 0)) == 0  # Expected: 0 neighbours
    assert world.get_neighbour_count((1, 1)) == 0  # Expected: 0 neighbours far away
    assert world.get_neighbour_count((1, 0)) == 1  # Expected: 1 neighbour at (0, 0)
    assert world.get_neighbour_count((-1, -1)) == 0  # Expected: 0 neighbours far away
    assert world.get_neighbour_count((2, 0)) == 0  # Expected: 0 neighbours far from the pattern

def test_still_life_block():
    # Still life — the two-by-two block reproduces itself exactly
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block pattern
    next_world = world.evolve()
    assert next_world.live_cells == world.live_cells  # Expected: remains the same

def test_still_life_beehive():
    # Still life — the beehive reproduces itself exactly
    world = World({(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)})  # Canonical beehive pattern
    next_world = world.evolve()
    assert next_world.live_cells == world.live_cells  # Expected: remains the same

def test_blinker():
    # The blinker alternates between vertical and horizontal
    world = World({(0, 1), (1, 1), (2, 1)})  # Horizontal blinker
    next_world = world.evolve()  # Step to vertical
    assert next_world.live_cells == {(1, 0), (1, 1), (1, 2)}  # Expected: vertical blinker
    next_next_world = next_world.evolve()  # Step back to horizontal
    assert next_next_world.live_cells == world.live_cells  # Expected: back to horizontal

def test_toad():
    # The toad changes shape after one generation and returns to its original shape after two
    world = World({(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)})  # Canonical toad
    next_world = world.evolve()  # Step to next shape
    assert next_world.live_cells == {(-1, 2), (0, 0), (0, 3), (1, 0), (1, 3), (2, 1)}  # Expected: changed shape
    next_next_world = next_world.evolve()  # Step back to original
    assert next_next_world.live_cells == world.live_cells  # Expected: back to original

def test_glider():
    # The glider translates itself diagonally by one cell every four generations
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})  # Initial glider
    next_world = world.evolve()  # Step 1
    next_next_world = next_world.evolve()  # Step 2
    next_next_next_world = next_next_world.evolve()  # Step 3
    fourth_world = next_next_next_world.evolve()  # Step 4
    assert fourth_world.live_cells == {(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)}  # Expected: moved diagonally

def test_world_from_text():
    # Build a world from rows of text
    text = ["*..", ".*.", "..*"]  # Text representation
    world = World.from_text(text)
    assert world.live_cells == {(0, 0), (1, 1), (2, 2)}  # Expected: live cells as per text

def test_world_to_text():
    # Render a world back to text with defined width and height
    world = World({(0, 0), (1, 1), (2, 2)})  # Initial live cells
    text = world.to_text(width=3, height=3)  # Specifying width and height
    assert text == ["*..", ".*.", "..*"]  # Expected text representation

def test_round_trip_text_conversion():
    # Ensure that parsing from text and rendering back matches
    text = ["*..", ".*.", "..*"]  # Text representation
    world = World.from_text(text)
    text_back = world.to_text(width=3, height=3)
    assert text_back == text  # Expected: text matches original

def test_equality_of_worlds():
    # Two worlds with the same live cells are equal
    world1 = World({(0, 0), (0, 1)})
    world2 = World({(0, 1), (0, 0)})  # Order should not matter
    assert world1 == world2  # Expected: they are equal

def test_hashing_of_worlds():
    # Hashing depends on the set of live cells
    world1 = World({(0, 0), (0, 1)})
    world2 = World({(0, 1), (0, 0)})  # Should hash to the same value
    assert hash(world1) == hash(world2)  # Expected: same hash
    world3 = World({(1, 1)})  # Different cells
    world4 = World({(1, 2)})  # Another distinct world
    # No assertion needed for specific hash values due to possible collisions

def test_population_of_empty_world():
    # An empty world reports population zero and empty live cells
    world = World(set())  # No live cells
    assert len(world.live_cells) == 0  # Expected: population zero

def test_evolve_retains_original_world():
    # Evolve returns a new world and leaves the original unchanged
    world = World({(0, 0), (0, 1)})  # Initial live cells
    next_world = world.evolve()
    assert world.live_cells == {(0, 0), (0, 1)}  # Original world unchanged
    assert next_world.live_cells != world.live_cells  # New world should be different

def test_far_coordinate_reports_dead():
    # Coordinates far from any pattern report dead
    world = World({(0, 0)})  # One live cell
    assert world.get_neighbour_count((100, 100)) == 0  # Expected: dead far away
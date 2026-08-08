from solution import World

def test_evolve_underpopulation():
    world = World({"(1, 0)"})  # A live cell at (1, 0) with zero neighbours
    new_world = world.evolve()
    assert new_world.live_cells == set()  # The cell dies of underpopulation

    world = World({"(0, 0)", "(1, 0)", "(2, 0)"})  # A horizontal blinker
    new_world = world.evolve()
    assert new_world.live_cells == {"(1, -1)", "(1, 0)", "(1, 1)"}  # The blinker evolves to vertical


def test_evolve_survival():
    world = World({"(0, 0)", "(1, 0)", "(1, 1)", "(2, 0)"})  # T-shape
    new_world = world.evolve()
    assert new_world.live_cells == {"(0, 0)", "(1, -1)", "(1, 0)", "(2, 0)", "(0, 1)", "(1, 1)", "(2, 1)"}  # All six cells survive


def test_evolve_overpopulation():
    world = World({"(0, 0)", "(1, 0)", "(1, 1)", "(2, 0)", "(0, 1)", "(2, 1)"})  # 3x2 rectangle
    new_world = world.evolve()
    assert new_world.live_cells == {"(1, -1)", "(0, 0)", "(2, 0)", "(0, 1)", "(2, 1)", "(1, 2)"}  # Four corners survive, others die


def test_evolve_reproduction():
    world = World({"(0, 0)", "(0, 1)", "(1, 0)"})  # L-shape
    new_world = world.evolve()
    assert new_world.live_cells == {"(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)"}  # The dead cell (1,1) becomes alive


def test_empty_world_stays_empty():
    world = World(set())  # An empty world
    new_world = world.evolve()
    assert new_world.live_cells == set()  # The world remains empty


def test_neighbourhood():
    world = World({"(1, 1)"})  # A single live cell
    assert world.count_neighbours((1, 1)) == 0  # No neighbours for itself
    assert world.count_neighbours((0, 0)) == 0  # No neighbours
    assert world.count_neighbours((1, 0)) == 1  # One neighbour at (1, 1)
    assert world.count_neighbours((2, 2)) == 0  # Far away
    assert world.count_neighbours((0, 1)) == 1  # One diagonal neighbour at (1, 1)
    assert world.count_neighbours((2, 1)) == 1  # One diagonal neighbour at (1, 1)
    assert world.count_neighbours((1, 2)) == 1  # One diagonal neighbour at (1, 1)
    assert world.count_neighbours((2, 0)) == 1  # One diagonal neighbour at (1, 1)


def test_still_life_block():
    world = World({"(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)"})  # Block
    new_world = world.evolve()
    assert new_world.live_cells == {"(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)"}  # Remains the same
    new_world = new_world.evolve()  # Check another generation
    assert new_world.live_cells == {"(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)"}  # Still remains the same


def test_still_life_beehive():
    world = World({"(1, 0)", "(2, 0)", "(0, 1)", "(3, 1)", "(1, 2)", "(2, 2)"})  # Beehive
    new_world = world.evolve()
    assert new_world.live_cells == {"(1, 0)", "(2, 0)", "(0, 1)", "(3, 1)", "(1, 2)", "(2, 2)"}  # Remains the same
    new_world = new_world.evolve()  # Check another generation
    assert new_world.live_cells == {"(1, 0)", "(2, 0)", "(0, 1)", "(3, 1)", "(1, 2)", "(2, 2)"}  # Still remains the same


def test_blinker():
    world = World({"(0, 1)", "(1, 1)", "(2, 1)"})  # Horizontal blinker
    new_world = world.evolve()  # First evolution: vertical
    assert new_world.live_cells == {"(1, 0)", "(1, 1)", "(1, 2)"}
    new_world = new_world.evolve()  # Second evolution: back to horizontal
    assert new_world.live_cells == {"(0, 1)", "(1, 1)", "(2, 1)"}


def test_toad():
    world = World({"(1, 0)", "(2, 0)", "(3, 0)", "(0, 1)", "(1, 1)", "(2, 1)"})  # Toad
    new_world = world.evolve()  # First evolution: new shape
    assert new_world.live_cells == {"(0, 0)", "(0, 1)", "(1, 1)", "(2, 1)", "(2, 2)"}  # Correct first phase
    new_world = new_world.evolve()  # Second evolution: back to original shape
    assert new_world.live_cells == {"(1, 0)", "(2, 0)", "(3, 0)", "(0, 1)", "(1, 1)", "(2, 1)"}


def test_glider():
    world = World({"(0, 1)", "(1, 2)", "(2, 0)", "(2, 1)", "(2, 2)"})  # Glider
    for _ in range(4):
        new_world = world.evolve()
        world = new_world
    assert new_world.live_cells == {"(1, 2)", "(2, 3)", "(3, 1)", "(3, 2)", "(3, 3)"}  # Assert position after 4 generations


def test_build_from_text():
    world = World.from_text(["*..", "...", ".*."])  # Building from text
    assert world.live_cells == {"(0, 0)", "(1, 2)"}


def test_render_to_text():
    world = World({"(0, 0)", "(1, 0)", "(1, 1)"})  # Cells to render
    text = world.render(3, 3) 
    assert text == ["**.", ".*.", "..."]  # Expected rendering


def test_round_trip_text():
    world = World.from_text(["*..", "...", ".*."])  # Building from text
    text = world.render(3, 3)
    assert text == ["*..", "...", ".*."]  # Renders back to the original text


def test_world_population_and_live_cells():
    world = World(set())  # An empty world
    assert world.population == 0  # Population is zero
    assert world.live_cells == set()  # Live cells is an empty set


def test_world_evolve_immutable():
    world = World({"(0, 0)", "(1, 0)"})  # Initial world
    new_world = world.evolve()  # Advance to next generation
    assert new_world.live_cells != world.live_cells  # The new world should be different
    assert world.live_cells == {"(0, 0)", "(1, 0)"}  # Original world should remain unchanged


def test_unbounded_plane():
    world = World({"(0, 0)"})  # Single live cell
    assert world.count_neighbours((1000, 1000)) == 0  # Distant coordinate reports dead
    assert world.count_neighbours((1000, 1000)) == 0  # Coordinate itself is dead


def test_world_equality():
    world1 = World({"(0, 0)", "(1, 1)"})
    world2 = World({"(1, 1)", "(0, 0)"})
    assert world1 == world2  # Same cells in different order


def test_world_hash():
    world1 = World({"(0, 0)", "(1, 1)"})
    world2 = World({"(1, 1)", "(0, 0)"})
    assert hash(world1) == hash(world2)  # Same hash for same cells

    world3 = World({"(0, 0)"})
    assert hash(world1) != hash(world3)  # Different hash for different cells


def test_reproduction_boundary():
    world = World({"(0, 0)", "(1, 0)"})  # Two live neighbours
    new_world = world.evolve()
    assert new_world.live_cells == set()  # Dead cell does not become alive with only two neighbours
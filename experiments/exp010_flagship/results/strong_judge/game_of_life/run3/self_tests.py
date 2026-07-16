from solution import World

def test_world_initialization_empty():
    world = World()
    assert world.live_cells == set()  # AC-4.1: An empty world has no live cells
    assert len(world.live_cells) == 0  # AC-4.1: Population is zero

def test_world_initialization_from_text():
    world = World.from_text(["*..", "...", ".*."])
    assert world.live_cells == {(0, 0), (2, 1)}  # AC-3.1: Convert text to live cells

def test_world_evolve_still_life_block():
    initial = World.from_text(["**", "**"])
    next_gen = initial.evolve()
    assert next_gen.live_cells == initial.live_cells  # AC-2.1: Block remains the same

def test_world_evolve_still_life_beehive():
    initial = World.from_text([".**.", "*..*", ".**."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == initial.live_cells  # AC-2.1: Beehive remains the same

def test_world_evolve_blinker():
    initial = World.from_text(["...", "***", "..."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == {(0, 1), (1, 1), (2, 1)}  # AC-2.2: Blinker becomes vertical
    next_gen = next_gen.evolve()
    assert next_gen.live_cells == initial.live_cells  # AC-2.2: Returns to original shape

def test_world_evolve_toad():
    initial = World.from_text(["...", ".***", "***."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == {(0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1)}  # AC-2.3: Toad changes
    next_gen = next_gen.evolve()
    assert next_gen.live_cells == initial.live_cells  # AC-2.3: Returns to original shape

def test_world_evolve_underpopulation():
    initial = World.from_text(["*.*", "...", "..."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == set()  # AC-1.1: Live cell dies from underpopulation

def test_world_evolve_survival_with_two_neighbours():
    initial = World.from_text(["*.*", "*..", "..."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == {(0, 1)}  # AC-1.2: Cell survives with 2 neighbours

def test_world_evolve_survival_three_neighbours():
    initial = World.from_text([".*.", "*.*", "..."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == {(0, 1), (1, 1)}  # AC-1.2: Cells survive with 3 neighbours

def test_world_evolve_overpopulation():
    initial = World.from_text(["***", "*.*", "***"])
    next_gen = initial.evolve()
    assert next_gen.live_cells == {(0, 0), (0, 2), (2, 0), (2, 2), (-1, 1), (1, -1), (1, 3), (3, 1)}  # AC-1.3: Correct overpopulation result

def test_world_evolve_reproduction():
    initial = World.from_text(["...", ".*.", "..."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == {(1, 0)}  # AC-1.4: Dead cell with exactly three neighbours becomes alive

def test_world_evolve_empty_remains_empty():
    initial = World()
    next_gen = initial.evolve()
    assert next_gen.live_cells == set()  # AC-1.5: Empty world stays empty

def test_world_neighbour_count():
    initial = World.from_text(["*..", "...", ".*."])
    count_alive = initial.neighbour_count((1, 1))  # Count neighbours for cell (1, 1)
    assert count_alive == 2  # AC-4.6: Two live neighbours

def test_world_rendering():
    world = World.from_text(["*..", "...", ".*."])
    rendered = world.render(3, 3)  # Render a 3x3 window
    assert rendered == ["*..", "...", ".*."]  # AC-3.2: Correct rendering as text

def test_world_equal_hashing():
    world1 = World.from_text(["*..", "...", ".*."])
    world2 = World.from_text([".*.", "...", "..*"])
    assert world1 == world2  # AC-4.4: Worlds with the same live cells are equal

def test_world_evolve_reproduction_boundary():
    initial = World.from_text(["...", ".*.", ".*."])
    next_gen = initial.evolve()
    assert next_gen.live_cells == set()  # AC-1.4: Dead cell remains dead with two neighbours

def test_world_neighbour_count_diagonal():
    initial = World.from_text(["*.*", "...", ".*."])
    assert initial.neighbour_count((1, 1)) == 2  # AC-4.6: Two live neighbours
    assert initial.neighbour_count((0, 0)) == 0  # AC-4.6: No neighbours for a far cell

def test_world_evolve_immutable():
    initial = World.from_text(["*.*", "*..", "..."])
    next_gen = initial.evolve()
    assert next_gen.live_cells != initial.live_cells  # New world is a distinct object
    assert initial.live_cells == {(0, 0), (0, 2), (1, 0)}  # Original world remains unchanged

def test_world_far_coordinate_dead_cell():
    world = World.from_text(["*"])
    assert (100, 100) not in world.live_cells  # AC-4.3: Far coordinate is dead

def test_world_hash_dependence():
    world1 = World.from_text(["*"])
    world2 = World.from_text(["*.", "."])
    assert hash(world1) == hash(world2)  # AC-4.5: Equal worlds have the same hash
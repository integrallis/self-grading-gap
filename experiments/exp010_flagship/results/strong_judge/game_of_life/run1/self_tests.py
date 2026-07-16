from solution import World

def test_empty_world():
    world = World()
    assert world.population() == 0  # No live cells means population is zero
    assert world.live_cells == set()  # No live cells means empty set

def test_advance_generation_empty_world():
    world = World()
    new_world = world.advance()
    assert new_world.population() == 0  # Advancing an empty world still results in an empty world
    assert world.live_cells == set()  # Original world remains unchanged

def test_live_cell_underpopulation():
    world = World({(0, 0)})  # A single live cell
    new_world = world.advance()
    assert new_world.population() == 0  # Underpopulation leads to death
    assert new_world.live_cells == set()  # No live cells should remain

def test_live_cell_survival():
    world = World({(0, 0), (1, 0), (0, 1)})  # A live cell with exactly two neighbours
    new_world = world.advance()
    assert new_world.population() == 4  # The live cells {(0, 0), (1, 0), (0, 1), (1, 1)} survive and the new born cell
    assert new_world.live_cells == {(0, 0), (1, 0), (0, 1), (1, 1)}  # Original cell survives and new cell is born

def test_live_cell_survival_three_neighbours():
    world = World({(0, 0), (1, 0), (0, 1), (1, 1)})  # A live cell with exactly three neighbours
    new_world = world.advance()
    assert new_world.population() == 4  # Survives with three neighbours and one new cell at (2, 1)
    assert new_world.live_cells == {(0, 0), (1, 0), (0, 1), (1, 1), (2, 1)}  # Original cells survive and a new cell is born

def test_live_cell_overpopulation():
    world = World({(0, 0), (1, 0), (0, 1), (1, 1), (2, 0)})  # A live cell with four neighbours
    new_world = world.advance()
    assert new_world.population() == 4  # Surviving cells are {(0, 0), (0, 1), (2, 0), (1, -1)} (two births) 
    assert new_world.live_cells == {(0, 0), (0, 1), (2, 0), (1, -1)}  # Surviving cells plus new births

def test_dead_cell_reproduction():
    world = World({(0, 0), (1, 0), (0, 1)})  # Three live cells surrounding a dead cell
    new_world = world.advance()
    assert new_world.population() == 4  # Four live cells including the new cell at (1, 1)
    assert new_world.live_cells == {(0, 0), (1, 0), (0, 1), (1, 1)}  # New cell at (1, 1)

def test_still_life_block():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # Block pattern
    new_world = world.advance()
    assert new_world.population() == 4  # Still life, population remains the same
    assert new_world.live_cells == world.live_cells  # No change in live cells

def test_still_life_beehive():
    world = World({(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)})  # Canonical beehive pattern
    new_world = world.advance()
    assert new_world.population() == 6  # Still life, population remains the same
    assert new_world.live_cells == world.live_cells  # No change in live cells

def test_blinker():
    world = World({(0, 0), (0, 1), (0, 2)})  # Horizontal blinker
    new_world = world.advance()
    assert new_world.live_cells == {(1, 0), (1, 1), (1, 2)}  # Should become vertical blinker
    new_world_next = new_world.advance()
    assert new_world_next.live_cells == world.live_cells  # Returns to original horizontal blinker

def test_toad():
    world = World({(0, 0), (0, 1), (1, 1), (1, 0), (2, 0), (2, 1)})  # Canonical toad pattern
    new_world = world.advance()
    assert new_world.live_cells == {(1, 0), (2, 0), (0, 1), (2, 1), (1, 1), (1, 2)}  # Changes shape
    new_world_next = new_world.advance()
    assert new_world_next.live_cells == world.live_cells  # Returns to original shape

def test_glider():
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})  # Glider pattern
    for _ in range(4):
        world = world.advance()
    assert world.live_cells == {(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)}  # Should have moved diagonally to this new position

def test_build_world_from_text():
    pattern = [
        ".*.",
        "***",
        ".*."
    ]
    world = World.from_text(pattern)
    assert world.live_cells == {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}  # Live cells from pattern

def test_render_world_to_text():
    world = World.from_text([
        ".*.",
        "***",
        ".*."
    ])  # Source pattern
    expected = [
        ".*.",
        "***",
        ".*."
    ]
    assert world.to_text(width=3, height=3) == expected  # Rendered output should match the input pattern

def test_world_equality():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (0, 0)})
    assert world1 == world2  # Should be equal regardless of order
    assert hash(world1) == hash(world2)  # Should hash the same

def test_world_inequality():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(0, 0), (1, 0)})
    assert world1 != world2  # Different live cells should not be equal

def test_neighbours_count():
    world = World({(0, 0), (1, 0), (0, 1)})  # Three live cells
    assert world.neighbour_count((0, 0)) == 2  # Cell (0, 0) has two live neighbours
    assert world.neighbour_count((1, 0)) == 2  # Cell (1, 0) has two live neighbours
    assert world.neighbour_count((0, 1)) == 2  # Cell (0, 1) has two live neighbours
    assert world.neighbour_count((2, 2)) == 0  # Empty cell far from live cells
    assert world.neighbour_count((0, 2)) == 1  # (0,2) is adjacent to (0,1) which is live
    assert world.neighbour_count((1, 1)) == 3  # Cell (1,1) has three live neighbours

def test_immutable_world():
    world = World({(0, 0), (1, 1)})  # Initial world with some live cells
    new_world = world.advance()  # Advance to a new world
    assert new_world != world  # New world should not be the same as the old one
    assert world.live_cells == {(0, 0), (1, 1)}  # Original world remains unchanged

def test_unbounded_plane():
    world = World({(0, 0)})  # A single live cell
    assert world.neighbour_count((100, 100)) == 0  # Distant cell should report dead

def test_adjacent_dead_cell_query():
    world = World({(0, 0), (1, 0)})  # Two live cells
    assert world.neighbour_count((0, 1)) == 1  # Cell (0, 1) is adjacent to (0, 0) which is live
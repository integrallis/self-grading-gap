from solution import World

def test_empty_world_has_no_live_cells():
    world = World()  # Create an empty world
    assert world.live_cells == set()  # No live cells

def test_empty_world_population_is_zero():
    world = World()  # Create an empty world
    assert world.population == 0  # Population is zero

def test_advance_empty_world_returns_empty_world():
    world = World()  # Create an empty world
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == set()  # Still no live cells
    assert next_world.population == 0  # Population remains zero

def test_live_cell_with_fewer_than_two_live_neighbors_dies():
    world = World(live_cells={(0, 0)})  # A single live cell
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == set()  # Cell dies

def test_live_cell_with_one_live_neighbor_dies():
    world = World(live_cells={(0, 0), (1, 0)})  # A live cell with one neighbor
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == set()  # Cell dies

def test_live_cell_with_two_live_neighbors_survives():
    world = World(live_cells={(0, 0), (0, 1), (1, 0)})  # A cell with 2 neighbors
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # Block formation

def test_live_cell_with_three_live_neighbors_survives():
    world = World(live_cells={(0, 0), (0, 1), (1, 0), (1, 1)})  # A stable block
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # No change

def test_live_cell_with_more_than_three_live_neighbors_dies():
    world = World(live_cells={(0, 0), (0, 1), (0, 2), (1, 1), (1, 0)})  # A cell with 4 neighbors
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == {(-1, 1), (0, 0), (0, 2), (1, 0), (1, 2)}  # Cell dies

def test_dead_cell_with_exactly_three_live_neighbors_becomes_alive():
    world = World(live_cells={(0, 0), (0, 1), (0, 2)})  # Three live neighbors around (1, 1)
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == {(-1, 1), (0, 1), (1, 1)}  # (1, 1) becomes alive

def test_dead_cell_with_two_live_neighbors_does_not_become_alive():
    world = World(live_cells={(0, 0), (0, 1)})  # Two live neighbors around (1, 1)
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == set()  # No change

def test_still_life_block_reproduces_itself():
    world = World(live_cells={(0, 0), (0, 1), (1, 0), (1, 1)})  # Block pattern
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == world.live_cells  # No change

def test_still_life_beehive_reproduces_itself():
    world = World(live_cells={(0, 1), (1, 0), (1, 2), (2, 1), (2, 2)})  # Beehive pattern
    next_world = world.advance()  # Advance the generation
    assert next_world.live_cells == world.live_cells  # No change

def test_blinker_changes_shape():
    world = World(live_cells={(0, 1), (1, 1), (2, 1)})  # Horizontal blinker
    next_world = world.advance()  # Next generation is vertical
    assert next_world.live_cells == {(1, 0), (1, 1), (1, 2)}  # Vertical form
    next_next_world = next_world.advance()  # Advance again
    assert next_next_world.live_cells == world.live_cells  # Back to horizontal

def test_toad_changes_shape():
    world = World(live_cells={(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)})  # Canonical Toad pattern
    next_world = world.advance()  # Next generation changes shape
    assert next_world.live_cells == {(-1, 2), (0, 0), (0, 3), (1, 0), (1, 3), (2, 1)}  # New shape
    next_next_world = next_world.advance()  # Advance again
    assert next_next_world.live_cells == world.live_cells  # Back to original shape

def test_glider_translates_diagonally():
    world = World(live_cells={(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})  # Glider pattern
    for _ in range(4):
        next_world = world.advance()  # Advance generation
        world = next_world  # Update world
    assert world.live_cells == {(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)}  # Glider moved diagonally

def test_world_can_be_built_from_text():
    world = World.from_text([".*.", "***", ".*."])  # Build from text
    assert world.live_cells == {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}  # Check live cells

def test_world_renders_to_text_with_dimensions():
    world = World(live_cells={(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)})  # Define a world
    text_representation = world.to_text(width=3, height=3)  # Render a 3x3 window
    expected_text = [".*.", "***", ".*."]  # Expected text
    assert text_representation == expected_text  # Check rendered text

def test_world_renders_parsing_back_to_text():
    world = World.from_text([".*.", "***", ".*."])  # Build from text
    text_representation = world.to_text(width=3, height=3)  # Render a 3x3 window
    assert text_representation == [".*.", "***", ".*."]  # Check exact round trip

def test_world_is_immutable():
    world = World(live_cells={(0, 0)})  # Create a world
    next_world = world.advance()  # Advance generation
    assert world.live_cells == {(0, 0)}  # Original world unchanged
    assert next_world.live_cells != world.live_cells  # Next world is different
    assert next_world is not world  # Ensure a new world object is returned

def test_two_worlds_with_same_live_cells_are_equal():
    world1 = World(live_cells={(0, 0), (1, 1)})  # First world
    world2 = World(live_cells={(1, 1), (0, 0)})  # Second world in different order
    assert world1 == world2  # Worlds should be equal

def test_two_worlds_with_same_live_cells_have_equal_hashes():
    world1 = World(live_cells={(0, 0), (1, 1)})  # First world
    world2 = World(live_cells={(1, 1), (0, 0)})  # Second world in different order
    assert hash(world1) == hash(world2)  # Equal hashes

def test_neighbour_count_for_live_cell():
    world = World(live_cells={(0, 0), (0, 1), (1, 0)})  # Define a world
    count = world.neighbour_count((0, 0))  # Count neighbours for (0, 0)
    assert count == 2  # Should have 2 live neighbours

def test_neighbour_count_for_dead_cell():
    world = World(live_cells={(0, 0), (0, 1), (1, 0)})  # Define a world
    count = world.neighbour_count((1, 1))  # Count neighbours for (1, 1)
    assert count == 3  # Should have 3 live neighbours

def test_neighbour_count_for_diagonal_cells():
    world = World(live_cells={(0, 0), (0, 1), (1, 0), (1, 1)})  # Define a world
    count = world.neighbour_count((0, 0))  # Count neighbours for (0, 0)
    assert count == 3  # Should have 3 live neighbours
    count = world.neighbour_count((0, 1))  # Count neighbours for (0, 1)
    assert count == 3  # Should have 3 live neighbours
    count = world.neighbour_count((1, 1))  # Count neighbours for (1, 1)
    assert count == 3  # Should have 3 live neighbours
    count = world.neighbour_count((-1, -1))  # Far away cell
    assert count == 0  # Should have 0 live neighbours

def test_default_dead_cell_far_away():
    world = World()  # Empty world
    assert (10**9, -10**9) not in world.live_cells  # Far away coordinate is dead
    assert world.neighbour_count((10**9, -10**9)) == 0  # Should have 0 live neighbours
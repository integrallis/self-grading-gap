from solution import World

def test_evolve_underpopulation():
    world = World({(0, 0), (1, 0)})  # two live cells
    new_world = world.evolve()  # evolves to a new world
    assert new_world.live_cells == set()  # underpopulation leads to all cells dying

def test_evolve_survival():
    world = World({(0, 0), (1, 0), (0, 1)})  # three live cells
    new_world = world.evolve()
    assert new_world.live_cells == {(0, 0), (1, 0), (0, 1)}  # survives

def test_evolve_overpopulation():
    world = World({(0, 0), (1, 0), (2, 0), (1, 1)})  # four live cells
    new_world = world.evolve()
    assert new_world.live_cells == {(1, 0), (2, 0), (1, 1)}  # cell (0, 0) dies due to overpopulation

def test_evolve_reproduction():
    world = World({(0, 0), (0, 1), (1, 0)})  # three live cells, dead cell (1, 1) should come to life
    new_world = world.evolve()
    assert new_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # (1, 1) becomes alive

def test_empty_world_stays_empty():
    world = World(set())  # empty world
    new_world = world.evolve()
    assert new_world.live_cells == set()  # remains empty

def test_neighbourhood():
    world = World({(0, 0)})  # single cell
    assert world.neighbour_count((0, 0)) == 0  # it has no neighbours
    assert world.neighbour_count((1, 1)) == 0  # far away cell

def test_still_life_block():
    world = World({(0, 0), (0, 1), (1, 0), (1, 1)})  # block pattern
    new_world = world.evolve()
    assert new_world.live_cells == {(0, 0), (0, 1), (1, 0), (1, 1)}  # remains unchanged

def test_still_life_beehive():
    world = World({(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)})  # beehive pattern
    new_world = world.evolve()
    assert new_world.live_cells == {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}  # remains unchanged

def test_blinker():
    world = World({(0, 1), (1, 1), (2, 1)})  # horizontal blinker
    new_world = world.evolve()  # becomes vertical
    assert new_world.live_cells == {(1, 0), (1, 1), (1, 2)}
    new_world = new_world.evolve()  # goes back to horizontal
    assert new_world.live_cells == {(0, 1), (1, 1), (2, 1)}

def test_toad():
    world = World({(0, 1), (1, 1), (2, 1), (1, 0), (2, 0)})  # toad pattern
    new_world = world.evolve()  # changes shape
    assert new_world.live_cells == {(1, 0), (0, 2), (1, 2), (2, 2), (2, 1)}
    new_world = new_world.evolve()  # returns to original
    assert new_world.live_cells == {(0, 1), (1, 1), (2, 1), (1, 0), (2, 0)}

def test_glider():
    world = World({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})  # glider pattern
    for _ in range(4):
        new_world = world.evolve()  # evolve 4 times
        world = new_world
    assert sorted(world.live_cells) == sorted({(1, 2), (2, 2), (2, 1), (3, 1), (3, 0)})  # translated by (1, 1)

def test_world_from_text():
    text = ["*..", "...", ".*."]
    world = World.from_text(text)
    assert world.live_cells == {(0, 0), (2, 1)}  # cells from the text

def test_render_world():
    world = World({(0, 0), (1, 0), (0, 1)})  # a small world
    rendered = world.render(3, 3)  # render a 3x3 window
    expected_rendering = ["***", "*..", "..."]  # expected rendering
    assert rendered == expected_rendering

def test_world_equality():
    world1 = World({(0, 0), (0, 1)})
    world2 = World({(0, 1), (0, 0)})  # same cells but different order
    assert world1 == world2  # should be equal

def test_world_hashing():
    world1 = World({(0, 0), (1, 1)})
    world2 = World({(1, 1), (0, 0)})  # same cells but different order
    assert hash(world1) == hash(world2)  # should have same hash
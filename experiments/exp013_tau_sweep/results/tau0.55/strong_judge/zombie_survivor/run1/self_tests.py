import pytest
from solution import Survivor, Game

def test_survivor_initialization():
    # A newly created survivor has:
    # - name: "Alice"
    # - wounds: 0
    # - alive: True
    # - actions: 3
    # - equipment: []
    # - experience: 0
    # - level: "Blue"
    survivor = Survivor(name="Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0
    assert survivor.alive is True
    assert survivor.actions == 3
    assert survivor.equipment == []
    assert survivor.experience == 0
    assert survivor.level == "Blue"
    assert survivor.skills == []  # No skills initially

def test_survivor_wounds():
    survivor = Survivor(name="Bob")
    survivor.take_wound()  # first wound
    assert survivor.wounds == 1
    assert survivor.alive is True
    survivor.take_wound()  # second wound
    assert survivor.wounds == 2
    assert survivor.alive is False
    survivor.take_wound()  # third wound, should be ignored
    assert survivor.wounds == 2

def test_survivor_equipment_load():
    survivor = Survivor(name="Charlie")
    for i in range(5):
        survivor.pick_up_equipment(f"Equipment {i+1}")
    assert survivor.equipment == ["Equipment 1", "Equipment 2", "Equipment 3", "Equipment 4", "Equipment 5"]
    
    # Attempt to pick up more equipment
    with pytest.raises(Exception, match="Charlie cannot carry any more equipment"):
        survivor.pick_up_equipment("Equipment 6")

def test_survivor_equipment_capacity_with_wounds():
    survivor = Survivor(name="Dave")
    survivor.pick_up_equipment("Equipment 1")
    survivor.pick_up_equipment("Equipment 2")
    survivor.pick_up_equipment("Equipment 3")  # 3 items in hand
    survivor.take_wound()  # wounds reduce capacity
    survivor.take_wound()  # now dead, capacity is 3
    # Attempt to pick up equipment now that Dave is dead
    with pytest.raises(Exception, match="Dave is dead"):
        survivor.pick_up_equipment("Equipment 4")
    assert survivor.equipment == ["Equipment 1", "Equipment 2", "Equipment 3"]  # Should remain unchanged

    # Now test capacity reduction with one wound and discard the last reserve item
    survivor = Survivor(name="Dave")
    for i in range(5):
        survivor.pick_up_equipment(f"Equipment {i+1}")
    survivor.take_wound()  # wounds reduce capacity
    assert survivor.equipment == ["Equipment 1", "Equipment 2", "Equipment 3", "Equipment 4"]  # Discard "Equipment 5"

def test_survivor_experience_and_level_up():
    survivor = Survivor(name="Eve")
    for _ in range(7):  # should reach level Yellow
        survivor.kill_zombie()
    assert survivor.experience == 7
    assert survivor.level == "Yellow"
    assert survivor.actions == 4  # +1 Action skill unlocked

    for _ in range(12):  # should reach level Orange
        survivor.kill_zombie()
    assert survivor.experience == 19
    assert survivor.level == "Orange"

    for _ in range(24):  # should reach level Red
        survivor.kill_zombie()
    assert survivor.experience == 43
    assert survivor.level == "Red"

def test_survivor_skill_choices():
    survivor = Survivor(name="Frank")
    for _ in range(19):  # should reach level Orange
        survivor.kill_zombie()
    assert survivor.level == "Orange"

    # At Orange, choices available are empty
    with pytest.raises(Exception, match="Frank has no skill choice available"):
        survivor.choose_skill("Hoard")  # should not be allowed

    # Now reach level Red
    for _ in range(24):  # should reach level Red
        survivor.kill_zombie()
    
    survivor.choose_skill("Hoard")  # choose first skill
    assert survivor.carrying_capacity == 6  # capacity increases

    # Attempt to choose second skill
    with pytest.raises(Exception, match="'Sniper' is not an available skill choice"):
        survivor.choose_skill("Sniper")  # should not be allowed

    survivor.choose_skill("Tough")  # choose available skill
    assert "Hoard" in survivor.skills  # skill should be added
    assert "Tough" in survivor.skills  # skill should be added

def test_game_initialization():
    game = Game()  # Using clock abstraction
    assert game.history == ["Game started at <timestamp>"]  # Check with actual timestamp in the final implementation
    assert len(game.survivors) == 0

def test_game_joining_survivors():
    game = Game()  # Using clock abstraction
    game.add_survivor("Gina")
    assert len(game.survivors) == 1
    assert game.history == ["Game started at <timestamp>", "Gina joined the game"]
    
    with pytest.raises(Exception, match="A survivor named 'Gina' already exists"):
        game.add_survivor("Gina")  # should fail

def test_game_ending_condition():
    game = Game()  # Using clock abstraction
    game.add_survivor("Hank")
    game.survivors[0].take_wound()  # Hank is alive
    assert game.is_over() is False
    game.survivors[0].take_wound()  # Hank now dead
    assert game.is_over() is True
    assert game.history[-1] == "The game has ended: all survivors died"

def test_game_multiple_survivors():
    game = Game()  # Using clock abstraction
    game.add_survivor("Alice")
    game.add_survivor("Bob")
    assert game.is_over() is False
    game.survivors[0].take_wound()
    game.survivors[1].take_wound()
    game.survivors[0].take_wound()  # Alice dies
    assert game.is_over() is False  # Game still active
    game.survivors[1].take_wound()  # Bob dies
    assert game.is_over() is True  # Now game ends

def test_game_dead_joiner_ends_game():
    game = Game()  # Using clock abstraction
    game.add_survivor("Charlie")
    game.survivors[0].take_wound()  # Charlie is alive
    game.survivors[0].take_wound()  # Charlie dies
    assert game.is_over() is True  # Game ends

    game.add_survivor("DeadBob")  # Adding a survivor already made dead
    assert game.is_over() is True  # Game still ends, doesn't change state

def test_game_level():
    game = Game()  # Using clock abstraction
    game.add_survivor("Alice")  # Should be Blue
    assert game.level == "Blue"
    game.survivors[0].kill_zombie()  # Gain XP
    assert game.level == "Blue"
    game.survivors[0].kill_zombie()  # More XP
    game.survivors[0].kill_zombie()
    game.survivors[0].kill_zombie()
    game.survivors[0].kill_zombie()
    game.survivors[0].kill_zombie()
    game.survivors[0].kill_zombie()  # Now reaches Yellow
    assert game.level == "Yellow"

def test_game_history():
    game = Game()  # Using clock abstraction
    game.add_survivor("Alice")
    game.survivors[0].pick_up_equipment("Axe")
    game.survivors[0].take_wound()
    game.survivors[0].take_wound()  # Alice dies
    assert game.history == [
        "Game started at <timestamp>",
        "Alice joined the game",
        "Alice acquired Axe",
        "Alice was wounded",
        "Alice died",
        "The game has ended: all survivors died"
    ]
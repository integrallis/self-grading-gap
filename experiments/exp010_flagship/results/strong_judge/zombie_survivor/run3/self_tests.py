import pytest
from solution import Survivor, Game

def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0  # AC-1.1
    assert survivor.is_alive is True  # AC-1.1
    assert survivor.actions_per_turn == 3  # AC-1.1
    assert survivor.equipment == []  # AC-1.1
    assert survivor.experience == 0  # AC-1.1
    assert survivor.level == "Blue"  # AC-1.1

def test_survivor_wounds():
    survivor = Survivor("Bob")
    survivor.take_wound()
    assert survivor.wounds == 1  # AC-1.2
    assert survivor.is_alive is True  # AC-1.2
    survivor.take_wound()
    assert survivor.wounds == 2  # AC-1.2
    assert survivor.is_alive is False  # AC-1.2
    survivor.take_wound()  # Wounds past death should be ignored
    assert survivor.wounds == 2  # AC-1.3

def test_survivor_equipment_load():
    survivor = Survivor("Charlie")
    for i in range(5):
        survivor.pick_up(f"Item {i+1}")
    assert len(survivor.equipment) == 5  # AC-2.1
    with pytest.raises(Exception) as e:
        survivor.pick_up("Item 6")
    assert str(e.value) == "Charlie cannot carry any more equipment"  # AC-2.2

def test_survivor_equipment_with_wounds():
    survivor = Survivor("Dave")
    for i in range(5):
        survivor.pick_up(f"Item {i+1}")
    survivor.take_wound()  # Wound reduces capacity to 4
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4"]  # AC-2.3
    with pytest.raises(Exception) as e:
        survivor.pick_up("Item 6")  # Should raise error since capacity is 4
    assert str(e.value) == "Dave cannot carry any more equipment"  # AC-2.2

def test_dead_survivor_pickup():
    survivor = Survivor("Eve")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    with pytest.raises(Exception) as e:
        survivor.pick_up("Item 1")
    assert str(e.value) == "Eve is dead"  # AC-2.4

def test_experience_and_level_up():
    survivor = Survivor("Frank")
    for _ in range(7):
        survivor.kill_zombie()  # Each kill gives 1 experience
    assert survivor.experience == 7  # AC-3.1
    assert survivor.level == "Yellow"  # AC-3.2
    assert survivor.actions_per_turn == 4  # AC-4.1

def test_skill_unlock_below_yellow():
    survivor = Survivor("Grace")
    for _ in range(6):
        survivor.kill_zombie()  # Stay Blue
    assert survivor.actions_per_turn == 3  # AC-4.1
    with pytest.raises(Exception) as e:
        survivor.choose_skill("Hoard")
    assert str(e.value) == "Grace has no skill choice available"  # AC-4.2

def test_skill_unlock_and_choice():
    survivor = Survivor("Grace")
    for _ in range(19):
        survivor.kill_zombie()  # Level up to Orange
    assert survivor.level == "Orange"  # AC-3.2
    available_skills = ["Hoard", "Sniper"]
    assert survivor.available_skills == available_skills  # AC-4.3
    with pytest.raises(Exception) as e:
        survivor.choose_skill("Tough")
    assert str(e.value) == "'Tough' is not an available skill choice"  # AC-4.5
    survivor.choose_skill("Hoard")  # Choose Hoard
    assert survivor.carrying_capacity == 6  # AC-4.4

def test_skill_choice_in_red():
    survivor = Survivor("Grace")
    for _ in range(50):
        survivor.kill_zombie()  # Level up to Red
    assert survivor.level == "Red"  # AC-3.2
    survivor.choose_skill("Hoard")  # Choose Hoard
    available_skills = survivor.available_skills
    assert available_skills == ["Sniper", "Tough"]  # Skills available at Red
    survivor.choose_skill("Sniper")  # Choose Sniper
    assert "Sniper" in survivor.skills  # Ensure Sniper is added to skills
    with pytest.raises(Exception) as e:
        survivor.choose_skill("Hoard")  # Hoard already held
    assert str(e.value) == "'Hoard' is not an available skill choice"  # AC-4.5

def test_second_action_in_red():
    survivor = Survivor("Grace")
    for _ in range(50):
        survivor.kill_zombie()  # Level up to Red
    assert survivor.actions_per_turn == 5  # AC-4.7

def test_game_management_start_and_end():
    clock = "2026-01-01T12:00:00"  # Deterministic clock for the test
    game = Game(clock)
    assert game.history == [f"Game started at {clock}"]  # AC-5.1
    survivor = game.add_survivor("Hank")
    survivor.take_wound()
    survivor.take_wound()  # Hank dies
    game.add_survivor("Ivy")  # Ivy is dead, should not create a second ending record
    assert game.is_over() is True  # AC-5.4
    assert game.history[-1] == "The game has ended: all survivors died"  # AC-6.2

def test_game_level_management():
    clock = "2026-01-01T12:00:00"  # Deterministic clock for the test
    game = Game(clock)
    survivor1 = game.add_survivor("Jack")
    for _ in range(7):
        survivor1.kill_zombie()  # Jack levels up to Yellow
    assert game.level == "Yellow"  # AC-5.6
    assert game.history[-1] == "Game level changed to Yellow"  # AC-6.3

def test_game_over_conditions():
    clock = "2026-01-01T12:00:00"  # Deterministic clock for the test
    game = Game(clock)  
    assert game.is_over() is False  # No survivors
    game.add_survivor("Hank")
    assert game.is_over() is False  # One living survivor
    survivor = game.add_survivor("Ivy")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    assert game.is_over() is True  # Hank dies, game ends

def test_history_records():
    clock = "2026-01-01T12:00:00"  # Deterministic clock for the test
    game = Game(clock)
    assert game.history == [f"Game started at {clock}"]  # AC-5.1
    survivor = game.add_survivor("Hank")
    assert game.history[-1] == "Hank joined the game"  # AC-6.1
    survivor.pick_up("Item 1")
    assert game.history[-1] == "Hank acquired Item 1"  # AC-6.1
    survivor.take_wound()
    assert game.history[-1] == "Hank was wounded"  # AC-6.1
    survivor.take_wound()
    assert game.history[-1] == "Hank died"  # AC-6.1
    assert game.history[-1] == "The game has ended: all survivors died"  # AC-6.2
import pytest
from solution import Survivor, Game
from datetime import datetime

def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0  # AC-1.1
    assert survivor.is_alive is True  # AC-1.1
    assert survivor.actions_per_turn == 3  # AC-1.1
    assert survivor.equipment == []  # AC-1.1
    assert survivor.experience == 0  # AC-1.1
    assert survivor.level == "Blue"  # AC-1.1
    assert survivor.available_skills == []  # AC-4.2

def test_survivor_wounds_and_life():
    survivor = Survivor("Bob")
    survivor.take_wound()
    assert survivor.wounds == 1  # AC-1.2
    assert survivor.is_alive is True  # AC-1.2
    survivor.take_wound()
    assert survivor.wounds == 2  # AC-1.2
    assert survivor.is_alive is False  # AC-1.2
    survivor.take_wound()  # Should not increase wounds past death
    assert survivor.wounds == 2  # AC-1.3

def test_survivor_equipment_load():
    survivor = Survivor("Charlie")
    for i in range(5):
        survivor.pick_up_equipment(f"Item {i+1}")
    assert len(survivor.equipment) == 5  # AC-2.2
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

    with pytest.raises(Exception) as excinfo:
        survivor.pick_up_equipment("Item 6")
    assert str(excinfo.value) == "Charlie cannot carry any more equipment"  # AC-2.2

    survivor.take_wound()
    with pytest.raises(Exception) as excinfo:
        survivor.pick_up_equipment("Item 6")  # Capacity now 4 after discarding last reserve item
    assert str(excinfo.value) == "Charlie cannot carry any more equipment"  # AC-2.2

    assert len(survivor.equipment) == 4  # Should now have 4 after discarding last reserve item
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4"]  # AC-2.3

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Dave")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    with pytest.raises(Exception) as excinfo:
        survivor.pick_up_equipment("Item 1")
    assert str(excinfo.value) == "Dave is dead"  # AC-2.4

def test_experience_and_level_up():
    survivor = Survivor("Eve")
    assert survivor.experience == 0  # Initial experience
    survivor.kill_zombie()  # 1 kill
    assert survivor.experience == 1  # AC-3.1
    assert survivor.level == "Blue"  # AC-3.2

    for _ in range(6):
        survivor.kill_zombie()  # 7 kills
    assert survivor.experience == 7  # AC-3.1
    assert survivor.level == "Yellow"  # AC-3.2

    for _ in range(11):  # 18 kills total
        survivor.kill_zombie()  
    assert survivor.experience == 18  # AC-3.1
    assert survivor.level == "Yellow"  # AC-3.2

    survivor.kill_zombie()  # 19 kills total
    assert survivor.experience == 19  # AC-3.1
    assert survivor.level == "Orange"  # AC-3.2

    for _ in range(24):  # 43 kills total
        survivor.kill_zombie()  
    assert survivor.experience == 43  # AC-3.1
    assert survivor.level == "Red"  # AC-3.2

    for _ in range(1):  # 44 kills total
        survivor.kill_zombie()  
    assert survivor.experience == 44  # AC-3.1
    assert survivor.level == "Red"  # AC-3.2

def test_unlock_skills():
    survivor = Survivor("Frank")
    assert survivor.actions_per_turn == 3  # AC-4.1
    assert survivor.available_skills == []  # AC-4.2

    survivor.kill_zombie()  # 1 kill
    survivor.kill_zombie()  # 2 kills
    survivor.kill_zombie()  # 3 kills
    survivor.kill_zombie()  # 4 kills
    survivor.kill_zombie()  # 5 kills
    survivor.kill_zombie()  # 6 kills
    assert survivor.experience == 6  # AC-3.1

    survivor.kill_zombie()  # 7 kills, reaches Yellow
    assert survivor.actions_per_turn == 4  # AC-4.1

    with pytest.raises(Exception) as excinfo:
        survivor.choose_skill("Hoard")
    assert str(excinfo.value) == "Frank has no skill choice available"  # AC-4.2

    survivor.kill_zombie()  # 8 kills
    survivor.kill_zombie()  # 9 kills
    survivor.kill_zombie()  # 10 kills
    survivor.kill_zombie()  # 11 kills
    survivor.kill_zombie()  # 12 kills
    survivor.kill_zombie()  # 13 kills
    survivor.kill_zombie()  # 14 kills
    survivor.kill_zombie()  # 15 kills
    survivor.kill_zombie()  # 16 kills
    survivor.kill_zombie()  # 17 kills
    survivor.kill_zombie()  # 18 kills, reaches Orange
    assert survivor.available_skills == ["Hoard", "Sniper"]  # AC-4.3

    survivor.choose_skill("Hoard")
    assert survivor.carrying_capacity == 6  # AC-4.4
    assert "Hoard" in survivor.skills  # Skill should be added

    with pytest.raises(Exception) as excinfo:
        survivor.choose_skill("Sniper")  # Should fail as Sniper is not available yet
    assert str(excinfo.value) == "'Sniper' is not an available skill choice"  # AC-4.5

    for _ in range(24):  # 42 kills total
        survivor.kill_zombie()  
    assert survivor.experience == 42  # AC-3.1
    assert survivor.level == "Red"  # AC-3.2

    survivor.choose_skill("Sniper")  # Sniper should be available now
    assert "Sniper" in survivor.skills  # Skill should be added

    survivor.kill_zombie()  # 43 kills
    survivor.kill_zombie()  # 44 kills
    survivor.kill_zombie()  # 45 kills
    survivor.kill_zombie()  # 46 kills
    survivor.kill_zombie()  # 47 kills
    survivor.kill_zombie()  # 48 kills
    survivor.kill_zombie()  # 49 kills
    survivor.kill_zombie()  # 50 kills, gain second "+1 Action"
    assert survivor.actions_per_turn == 5  # AC-4.7

def test_game_management():
    clock = lambda: datetime.now().isoformat()
    game = Game(clock)
    assert game.history == [f"Game started at {clock()}"]  # AC-5.1
    survivor = game.add_survivor("Grace")
    assert survivor.name == "Grace"  # AC-5.2

    with pytest.raises(Exception) as excinfo:
        game.add_survivor("Grace")  # Duplicate name
    assert str(excinfo.value) == "A survivor named 'Grace' already exists"  # AC-5.3

    survivor.take_wound()
    survivor.take_wound()  # Dead survivor
    assert game.is_over() is True  # Game should end now
    assert game.history[-1] == "The game has ended: all survivors died"  # AC-5.2

    survivor2 = game.add_survivor("Hank")  # Hank joins
    assert survivor2.name == "Hank"  # AC-5.2
    assert game.is_over() is False  # Game should not be over

def test_game_level():
    clock = lambda: datetime.now().isoformat()
    game = Game(clock)
    survivor1 = game.add_survivor("Ivy")
    survivor2 = game.add_survivor("Jack")

    assert game.level == "Blue"  # AC-5.6
    survivor1.kill_zombie()  # Increase experience
    survivor1.kill_zombie()  # Increase experience
    survivor1.kill_zombie()  # Increase experience
    survivor1.kill_zombie()  # Increase experience
    survivor1.kill_zombie()  # Increase experience
    survivor1.kill_zombie()  # Increase experience
    survivor1.kill_zombie()  # Increase experience
    assert game.level == "Blue"  # AC-5.6
    survivor1.kill_zombie()  # 7 kills
    assert game.level == "Yellow"  # AC-5.6

    survivor2.kill_zombie()  # Increase experience
    survivor2.kill_zombie()  # Increase experience
    survivor2.kill_zombie()  # Increase experience
    survivor2.kill_zombie()  # Increase experience
    survivor2.kill_zombie()  # Increase experience
    survivor2.kill_zombie()  # Increase experience
    survivor2.kill_zombie()  # Increase experience
    assert game.level == "Yellow"  # AC-5.6

    survivor2.kill_zombie()  # 8 kills
    survivor2.kill_zombie()  # 9 kills
    survivor2.kill_zombie()  # 10 kills
    survivor2.kill_zombie()  # 11 kills
    survivor2.kill_zombie()  # 12 kills
    survivor2.kill_zombie()  # 13 kills
    survivor2.kill_zombie()  # 14 kills
    survivor2.kill_zombie()  # 15 kills
    survivor2.kill_zombie()  # 16 kills
    survivor2.kill_zombie()  # 17 kills
    survivor2.kill_zombie()  # 18 kills, reaches Orange
    assert game.level == "Orange"  # AC-5.6

    survivor1.kill_zombie()  # 8 kills
    survivor1.kill_zombie()  # 9 kills
    survivor1.kill_zombie()  # 10 kills
    survivor1.kill_zombie()  # 11 kills
    survivor1.kill_zombie()  # 12 kills
    survivor1.kill_zombie()  # 13 kills
    survivor1.kill_zombie()  # 14 kills
    survivor1.kill_zombie()  # 15 kills
    survivor1.kill_zombie()  # 16 kills
    survivor1.kill_zombie()  # 17 kills
    survivor1.kill_zombie()  # 18 kills
    survivor1.kill_zombie()  # 19 kills, reaches Orange
    assert game.level == "Orange"  # AC-5.6

    survivor1.kill_zombie()  # 20 kills
    survivor1.kill_zombie()  # 21 kills
    survivor1.kill_zombie()  # 22 kills
    survivor1.kill_zombie()  # 23 kills
    survivor1.kill_zombie()  # 24 kills
    survivor1.kill_zombie()  # 25 kills
    survivor1.kill_zombie()  # 26 kills
    survivor1.kill_zombie()  # 27 kills
    survivor1.kill_zombie()  # 28 kills
    survivor1.kill_zombie()  # 29 kills
    survivor1.kill_zombie()  # 30 kills
    survivor1.kill_zombie()  # 31 kills
    survivor1.kill_zombie()  # 32 kills
    survivor1.kill_zombie()  # 33 kills
    survivor1.kill_zombie()  # 34 kills
    survivor1.kill_zombie()  # 35 kills
    survivor1.kill_zombie()  # 36 kills
    survivor1.kill_zombie()  # 37 kills
    survivor1.kill_zombie()  # 38 kills
    survivor1.kill_zombie()  # 39 kills
    survivor1.kill_zombie()  # 40 kills
    survivor1.kill_zombie()  # 41 kills
    survivor1.kill_zombie()  # 42 kills
    survivor1.kill_zombie()  # 43 kills, reaches Red
    assert game.level == "Red"  # AC-5.6
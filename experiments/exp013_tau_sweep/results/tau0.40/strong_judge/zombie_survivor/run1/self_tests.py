import pytest
from solution import Survivor, Game
from datetime import datetime

def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0  # AC-1.1
    assert survivor.is_alive is True  # AC-1.1
    assert survivor.actions == 3  # AC-1.1
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
    survivor.take_wound()
    assert survivor.wounds == 2  # AC-1.3

def test_survivor_equipment_load():
    survivor = Survivor("Charlie")
    for i in range(5):
        survivor.pick_up(f"Item {i + 1}")
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]  # AC-2.1
    with pytest.raises(Exception) as excinfo:
        survivor.pick_up("Item 6")
    assert str(excinfo.value) == "Charlie cannot carry any more equipment"  # AC-2.2

def test_survivor_equipment_load_with_wounds():
    survivor = Survivor("David")
    for i in range(5):
        survivor.pick_up(f"Item {i + 1}")
    survivor.take_wound()  # Capacity reduced to 4
    survivor.pick_up("Item 6")  # Should discard Item 5
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4", "Item 6"]  # AC-2.3
    with pytest.raises(Exception) as excinfo:
        survivor.pick_up("Item 7")  # Should raise error due to capacity
    assert str(excinfo.value) == "David cannot carry any more equipment"  # AC-2.2

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Eve")
    survivor.take_wound()
    survivor.take_wound()
    with pytest.raises(Exception) as excinfo:
        survivor.pick_up("Item 1")
    assert str(excinfo.value) == "Eve is dead"  # AC-2.4

def test_experience_and_level_up():
    survivor = Survivor("Frank")
    for _ in range(6):
        survivor.kill_zombie()
    assert survivor.experience == 6  # AC-3.1
    assert survivor.level == "Blue"  # AC-3.2
    survivor.kill_zombie()
    assert survivor.experience == 7  # AC-3.1
    assert survivor.level == "Yellow"  # AC-3.2

def test_level_boundaries():
    survivor = Survivor("Grace")
    for _ in range(18):
        survivor.kill_zombie()
    assert survivor.experience == 18  # AC-3.2
    assert survivor.level == "Yellow"  # AC-3.2
    survivor.kill_zombie()
    assert survivor.experience == 19  # AC-3.1
    assert survivor.level == "Orange"  # AC-3.2
    for _ in range(23):  # 19 to 42
        survivor.kill_zombie()
    assert survivor.experience == 42  # AC-3.2
    assert survivor.level == "Orange"  # AC-3.2
    survivor.kill_zombie()  # Should reach Red
    assert survivor.experience == 43  # AC-3.1
    assert survivor.level == "Red"  # AC-3.2

def test_skills_unlocking():
    survivor = Survivor("Hank")
    assert survivor.actions == 3  # below Yellow, AC-4.1
    for _ in range(7):
        survivor.kill_zombie()
    assert survivor.actions == 4  # reached Yellow, AC-4.1
    with pytest.raises(Exception) as excinfo:
        survivor.choose_skill("Hoard")
    assert str(excinfo.value) == "Hank has no skill choice available"  # AC-4.2
    for _ in range(12):
        survivor.kill_zombie()
    assert survivor.actions == 4  # still Yellow
    assert survivor.available_skills == ["Hoard", "Sniper"]  # reached Orange, AC-4.3

def test_skill_choice_and_capacity():
    survivor = Survivor("Ivy")
    for _ in range(19):
        survivor.kill_zombie()
    assert survivor.available_skills == ["Hoard", "Sniper"]  # AC-4.3
    survivor.choose_skill("Hoard")
    assert survivor.max_load == 6  # AC-4.4

def test_invalid_skill_choice():
    survivor = Survivor("Jack")
    for _ in range(19):
        survivor.kill_zombie()
    survivor.choose_skill("Hoard")
    with pytest.raises(Exception) as excinfo:
        survivor.choose_skill("Sniper")  # Sniper is not an available skill choice
    assert str(excinfo.value) == "'Sniper' is not an available skill choice"  # AC-4.5

def test_red_skill_choice():
    survivor = Survivor("Kara")
    for _ in range(43):
        survivor.kill_zombie()
    survivor.choose_skill("Hoard")
    assert survivor.available_skills == ["Sniper", "Tough"]  # AC-4.6
    survivor.choose_skill("Sniper")  # Choosing a new skill
    assert "Hoard" not in survivor.available_skills  # Hoard is no longer available

def test_game_management():
    clock = datetime(2026, 1, 1, 12, 0, 0)
    game = Game(clock)
    assert game.survivors == []  # AC-5.1
    assert game.history[0] == "Game started at 2026-01-01T12:00:00"  # AC-5.1
    survivor = Survivor("Liam")
    game.add_survivor(survivor)
    assert game.survivors == [survivor]  # AC-5.2
    with pytest.raises(Exception) as excinfo:
        game.add_survivor(survivor)
    assert str(excinfo.value) == "A survivor named 'Liam' already exists"  # AC-5.3
    assert game.level == "Blue"  # AC-5.6

def test_game_end_condition():
    game = Game(datetime.now())
    survivor1 = Survivor("Mia")
    survivor2 = Survivor("Noah")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)
    survivor1.take_wound()
    survivor1.take_wound()
    survivor2.take_wound()
    survivor2.take_wound()
    assert game.is_over() is False  # AC-5.4
    survivor1.take_wound()  # survivor1 dies
    survivor2.take_wound()  # survivor2 dies
    assert game.is_over() is True  # AC-5.4
    assert game.history.count("The game has ended: all survivors died") == 1  # AC-6.2

def test_empty_game_is_not_over():
    game = Game(datetime.now())
    assert game.is_over() is False  # Empty game not over

def test_living_survivor_keeps_game_ongoing():
    game = Game(datetime.now())
    survivor = Survivor("Oliver")
    game.add_survivor(survivor)
    survivor.take_wound()
    assert game.is_over() is False  # One living survivor keeps game ongoing

def test_game_level_is_highest_among_living_survivors():
    game = Game(datetime.now())
    survivor1 = Survivor("Parker")
    survivor2 = Survivor("Quinn")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)
    for _ in range(6):
        survivor1.kill_zombie()  # Blue
    for _ in range(19):
        survivor2.kill_zombie()  # Orange
    assert game.level == "Orange"  # Highest level among living survivors

def test_dead_survivors_do_not_contribute_to_game_level():
    game = Game(datetime.now())
    survivor1 = Survivor("Riley")
    survivor2 = Survivor("Sophie")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)
    survivor1.take_wound()
    survivor1.take_wound()  # Dead
    for _ in range(19):
        survivor2.kill_zombie()  # Orange
    assert game.level == "Orange"  # Only survivor2 contributes

def test_history_records():
    game = Game(datetime.now())
    survivor = Survivor("Toby")
    game.add_survivor(survivor)
    assert game.history[-1] == "Toby joined the game"  # Join record
    survivor.kill_zombie()
    survivor.kill_zombie()  # Kills do not produce history
    survivor.take_wound()
    assert game.history[-1] == "Toby was wounded"  # Wound record
    survivor.take_wound()
    assert game.history[-1] == "Toby died"  # Death record

def test_game_level_change_history():
    game = Game(datetime.now())
    survivor1 = Survivor("Ursula")
    survivor2 = Survivor("Victor")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)
    for _ in range(6):
        survivor1.kill_zombie()  # Blue
    for _ in range(7):
        survivor2.kill_zombie()  # Yellow
    assert game.history.count("Game level changed to Yellow") == 1  # Level change record
    for _ in range(12):
        survivor2.kill_zombie()  # Orange
    assert game.history.count("Game level changed to Orange") == 1  # Level change record
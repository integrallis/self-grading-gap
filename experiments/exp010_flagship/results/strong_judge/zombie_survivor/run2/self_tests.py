from solution import Survivor, Game
import pytest
from datetime import datetime

class MockClock:
    def now(self):
        return datetime.fromisoformat("2026-01-01T12:00:00")

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
    survivor.take_wound()  # Should be ignored
    assert survivor.wounds == 2  # AC-1.3

def test_survivor_equipment_load():
    survivor = Survivor("Charlie")
    survivor.pick_up("Sword")
    survivor.pick_up("Shield")
    survivor.pick_up("Axe")
    survivor.pick_up("Bow")
    survivor.pick_up("Potion")
    assert survivor.equipment == ["Sword", "Shield", "Axe", "Bow", "Potion"]  # AC-2.1
    with pytest.raises(Exception, match="^Charlie cannot carry any more equipment$"):
        survivor.pick_up("Hammer")  # Should be refused

def test_survivor_wounded_carrying_capacity():
    survivor = Survivor("Diana")
    survivor.pick_up("Sword")
    survivor.pick_up("Shield")
    survivor.pick_up("Axe")
    survivor.pick_up("Bow")
    survivor.pick_up("Potion")  # 5 items
    survivor.take_wound()  # 1 wound reduces capacity to 4
    assert survivor.can_carry() == 4  # AC-2.3
    survivor.pick_up("Hammer")  # Should discard the last piece (Potion)
    assert survivor.equipment == ["Sword", "Shield", "Axe", "Bow"]  # AC-2.3
    assert survivor.can_carry() == 4  # AC-2.3

def test_dead_survivor_cannot_pick_up():
    survivor = Survivor("Eve")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    with pytest.raises(Exception, match="^Eve is dead$"):
        survivor.pick_up("Sword")  # Should be refused

def test_survivor_experience_and_level_up():
    survivor = Survivor("Frank")
    for _ in range(6):  # Earn 6 experience, should still be Blue
        survivor.kill_zombie()
    assert survivor.experience == 6  # AC-3.1
    assert survivor.level == "Blue"  # AC-3.2

    survivor.kill_zombie()  # Earn experience to level up
    assert survivor.experience == 7  # AC-3.1
    assert survivor.level == "Yellow"  # AC-3.2

    for _ in range(11):  # Earn 11 more experience to reach Orange
        survivor.kill_zombie()
    assert survivor.experience == 18  # AC-3.1
    assert survivor.level == "Yellow"  # AC-3.2  # FIXED

    survivor.kill_zombie()  # Earn experience to level up to Red
    assert survivor.experience == 19  # AC-3.1
    assert survivor.level == "Orange"  # AC-3.2  # FIXED

    for _ in range(24):  # Earn 24 more experience to reach Red
        survivor.kill_zombie()
    assert survivor.experience == 43  # AC-3.1
    assert survivor.level == "Red"  # AC-3.2

    survivor.kill_zombie()  # Earn experience to level up
    assert survivor.experience == 44  # AC-3.1
    assert survivor.level == "Red"  # AC-3.2

def test_survivor_skills():
    survivor = Survivor("Gina")
    assert survivor.actions_per_turn == 3  # AC-4.1
    for _ in range(7):  # Advance to Yellow
        survivor.kill_zombie()
    assert survivor.actions_per_turn == 4  # AC-4.1
    with pytest.raises(Exception, match="^Gina has no skill choice available$"):
        survivor.choose_skill("Hoard")  # No choice below Orange

    for _ in range(12):  # Advance to Orange
        survivor.kill_zombie()

    assert survivor.choose_skill("Hoard")  # Should be valid
    assert survivor.skills == ["Hoard"]  # AC-4.3, AC-4.4
    assert survivor.can_carry() == 6  # AC-4.4

def test_game_management():
    clock = MockClock()
    game = Game(clock)
    assert game.history == ["Game started at 2026-01-01T12:00:00"]  # AC-5.1
    survivor = game.add_survivor("Hank")
    assert game.history[-1] == "Hank joined the game"  # AC-6.1

    with pytest.raises(Exception, match="^A survivor named 'Hank' already exists$"):
        game.add_survivor("Hank")  # Duplicate name

    game.add_survivor("Ivy")  # Add another survivor
    assert game.get_level() == "Blue"  # AC-5.6

    survivor.take_wound()
    survivor.take_wound()  # Hank dies
    assert not survivor.is_alive  # Confirm dead
    assert game.is_over() is False  # Still alive survivors
    game.add_survivor("Jack")  # Add a new survivor
    assert game.get_level() == "Blue"  # AC-5.6

    survivor2 = game.add_survivor("DeadSurvivor")  # Add a dead survivor
    survivor2.take_wound()
    survivor2.take_wound()  # Dead
    game.check_end_game()  # Now check if the game ends
    assert game.is_over() is True  # All survivors dead
    assert game.history[-1] == "The game has ended: all survivors died"  # AC-6.2

def test_game_not_over_with_no_survivors():
    clock = MockClock()
    game = Game(clock)
    assert game.is_over() is False  # New game has no survivors, so not over

def test_survivor_order():
    clock = MockClock()
    game = Game(clock)
    survivor1 = game.add_survivor("Alice")
    survivor2 = game.add_survivor("Bob")
    survivors = game.get_survivors()
    assert survivors == ["Alice", "Bob"]  # Check joining order

def test_game_level_follows_highest_survivor():
    clock = MockClock()
    game = Game(clock)
    survivor1 = game.add_survivor("Alice")
    assert game.get_level() == "Blue"  # Only Alice is Blue
    survivor1.kill_zombie()  # Alice levels up to Yellow
    assert game.get_level() == "Yellow"  # Game level updates to Yellow
    survivor2 = game.add_survivor("Bob")
    for _ in range(6):
        survivor2.kill_zombie()  # Level Bob to Blue
    assert game.get_level() == "Yellow"  # Still Yellow
    for _ in range(11):
        survivor2.kill_zombie()  # Level Bob to Orange
    assert game.get_level() == "Orange"  # Game level updates to Orange
    for _ in range(24):
        survivor2.kill_zombie()  # Level Bob to Red
    assert game.get_level() == "Red"  # Game level updates to Red

def test_game_does_not_record_second_end_history_entry():
    clock = MockClock()
    game = Game(clock)
    survivor1 = game.add_survivor("Alice")
    survivor1.take_wound()
    survivor1.take_wound()  # Alice dies
    game.check_end_game()  # Check if the game ends
    assert game.is_over() is True  # All survivors dead
    assert game.history.count("The game has ended: all survivors died") == 1  # Only one end entry
    survivor2 = game.add_survivor("Bob")
    survivor2.take_wound()
    survivor2.take_wound()  # Bob dies
    game.check_end_game()  # Check again
    assert game.is_over() is True  # Still all dead
    assert game.history.count("The game has ended: all survivors died") == 1  # Still only one end entry

def test_event_announcements():
    clock = MockClock()
    game = Game(clock)
    survivor = game.add_survivor("Alice")
    events = []
    
    def listener(event_type, message):
        events.append((event_type, message))

    survivor.register_listener(listener)
    survivor.pick_up("Sword")
    assert events[-1] == ("acquired", "Alice acquired Sword")  # AC-6.4
    survivor.take_wound()
    assert events[-1] == ("wounded", "Alice was wounded")  # AC-6.4
    survivor.kill_zombie()  # No level-up
    assert len(events) == 2  # No new event

    for _ in range(6):  # Leveling up to Yellow
        survivor.kill_zombie()
    assert events[-1] == ("level-up", "Alice advanced to Yellow")  # AC-6.4
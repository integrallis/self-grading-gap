import pytest
from solution import Game, Survivor  # Assuming these are the correct imports

# Test for US-1: Track a survivor's wounds and life
def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0  # AC-1.1: newly created survivor has no wounds
    assert survivor.is_alive()  # AC-1.1: survivor is alive
    assert survivor.actions == 3  # AC-1.1: can take three actions per turn
    assert survivor.equipment == []  # AC-1.1: carries nothing
    assert survivor.experience == 0  # AC-1.1: has zero experience
    assert survivor.level == "Blue"  # AC-1.1: at level Blue

def test_survivor_wounds():
    survivor = Survivor("Bob")
    survivor.take_wound()  # One wound
    assert survivor.wounds == 1  # AC-1.2: one wound leaves survivor alive
    survivor.take_wound()  # Second wound
    assert survivor.wounds == 2  # AC-1.2: second wound kills survivor
    assert not survivor.is_alive()  # Survivor is now dead
    survivor.take_wound()  # Third wound, should be ignored
    assert survivor.wounds == 2  # AC-1.3: count never rises beyond two

# Test for US-2: Manage a survivor's equipment load
def test_equipment_load():
    survivor = Survivor("Charlie")
    for i in range(5):
        survivor.pick_up_equipment(f"Item {i+1}")  # Pick up 5 items
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]  # AC-2.1: fills "in hand" first

    with pytest.raises(Exception) as excinfo:
        survivor.pick_up_equipment("Item 6")  # Attempt to pick up a 6th item
    assert str(excinfo.value) == "Charlie cannot carry any more equipment"  # AC-2.2: cannot carry more

def test_equipment_wounds():
    survivor = Survivor("Dana")
    for i in range(5):
        survivor.pick_up_equipment(f"Item {i+1}")  # Pick up 5 items
    survivor.take_wound()  # First wound
    assert survivor.max_equipment == 4  # AC-2.3: capacity reduced to 4
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 4"]  # AC-2.3: Item 5 must be discarded
    survivor.pick_up_equipment("Item 6")  # Should discard "Item 5" to fit the new capacity
    assert survivor.equipment == ["Item 1", "Item 2", "Item 3", "Item 6"]  # AC-2.3: most recent reserve piece discarded

    with pytest.raises(Exception) as excinfo:
        survivor.pick_up_equipment("Item 7")  # Attempt to pick up a 6th item
    assert str(excinfo.value) == "Dana cannot carry any more equipment"  # AC-2.2: cannot carry more

def test_dead_survivor_equipment_pickup():
    survivor = Survivor("Eve")
    survivor.take_wound()  # First wound
    survivor.take_wound()  # Second wound kills Eve
    with pytest.raises(Exception) as excinfo:
        survivor.pick_up_equipment("Item 1")  # Attempt to pick up equipment while dead
    assert str(excinfo.value) == "Eve is dead"  # AC-2.4: dead survivor cannot pick up equipment

# Test for US-3: Earn experience and level up
def test_experience_and_level():
    survivor = Survivor("Frank")
    for _ in range(6):
        survivor.kill_zombie()  # Each kill earns 1 experience
    assert survivor.experience == 6  # AC-3.1: 6 experience from 6 kills
    assert survivor.level == "Blue"  # Still level Blue

    # Level up by killing more zombies
    survivor.kill_zombie()  # 7 experience
    assert survivor.level == "Yellow"  # AC-3.2: level changes to Yellow

    for _ in range(11):
        survivor.kill_zombie()  # Reach 18 experience
    assert survivor.level == "Yellow"  # Still level Yellow

    survivor.kill_zombie()  # 19 experience
    assert survivor.level == "Orange"  # AC-3.2: level changes to Orange

    for _ in range(23):
        survivor.kill_zombie()  # Reach 42 experience
    assert survivor.level == "Red"  # AC-3.2: level changes to Red

    survivor.kill_zombie()  # 43 experience
    assert survivor.level == "Red"  # Still level Red

    for _ in range(7):
        survivor.kill_zombie()  # Reach 50 experience
    assert survivor.actions == 5  # AC-4.7: receives second +1 Action skill

# Test for US-4: Unlock and choose skills
def test_skills_unlocked():
    survivor = Survivor("Gina")
    for _ in range(6):
        survivor.kill_zombie()  # Level up to Blue max
    survivor.kill_zombie()  # Reach Yellow
    assert survivor.actions == 4  # AC-4.1: receives +1 Action skill
    assert survivor.skills == []  # AC-4.2: no skills below Orange

    # Reaching Orange
    for _ in range(12):
        survivor.kill_zombie()  # Reach Orange
    assert survivor.skills == []  # AC-4.3: still no skills to choose from

    # Choose skills at Orange
    survivor.choose_skill("Hoard")  # Should succeed
    assert survivor.skills == ["Hoard"]  # AC-4.4: skill added
    assert survivor.max_equipment == 6  # Carrying capacity increased

    with pytest.raises(Exception) as excinfo:
        survivor.choose_skill("Sniper")  # Invalid choice, should not be possible yet
    assert str(excinfo.value) == "'Sniper' is not an available skill choice"  # AC-4.5: invalid choice

    # Reach Red
    for _ in range(4):
        survivor.kill_zombie()  # Level up to Red
    assert survivor.skills == ["Hoard"]  # Still has Hoard
    survivor.choose_skill("Tough")  # Choose Tough
    assert survivor.skills == ["Hoard", "Tough"]  # AC-4.6: skill added

# Test for US-5: Run the game roster, level, and end condition
def test_game_management():
    game = Game("2026-01-01T12:00:00")  # Injecting a deterministic clock
    assert game.history == ["Game started at 2026-01-01T12:00:00"]  # AC-5.1: history starts with game start

    survivor = game.add_survivor("Gina")
    assert game.survivors == [survivor]  # AC-5.2: survivor added
    with pytest.raises(Exception) as excinfo:
        game.add_survivor("Gina")  # Duplicate survivor
    assert str(excinfo.value) == "A survivor named 'Gina' already exists"  # AC-5.3: duplicate name

    survivor.take_wound()  # Wound survivor
    survivor.take_wound()  # Kill survivor
    assert not survivor.is_alive()  # Survivor is dead
    assert not game.is_over()  # Game is not over with only one dead survivor

    game.add_survivor("Hank")  # Add a new survivor
    survivor2 = game.add_survivor("Ivy")
    survivor2.take_wound()  # Wound Ivy
    survivor2.take_wound()  # Kill Ivy
    assert game.is_over()  # Game ends when all survivors are dead

    game.add_survivor("Jack")  # Add another survivor
    assert not game.is_over()  # Game should still not be over

    game.add_survivor("Kara")  # Add yet another survivor
    assert not game.is_over()  # Game still not over

    # Test for a new game with no survivors is not over
    new_game = Game("2026-01-01T12:00:00")
    assert not new_game.is_over()  # Game should not be over

# Test for US-6: Keep a history and announce survivor events
def test_history_recording():
    game = Game("2026-01-01T12:00:00")  # Using a deterministic clock
    survivor = game.add_survivor("Jack")
    assert game.history == ["Game started at 2026-01-01T12:00:00", "Jack joined the game"]  # AC-6.1

    survivor.pick_up_equipment("Baseball Bat")
    assert game.history[-1] == "Jack acquired Baseball Bat"  # AC-6.1: picking up equipment

    survivor.take_wound()
    assert game.history[-1] == "Jack was wounded"  # AC-6.1: taking a wound

    survivor.take_wound()  # Second wound kills
    assert game.history[-1] == "Jack died"  # AC-6.1: death recorded

    assert game.history.count("The game has ended: all survivors died") == 0  # Game not over yet
    game.add_survivor("Liam").take_wound()  # Wound Liam
    game.add_survivor("Mona").take_wound()  # Wound Mona

    survivor2 = game.add_survivor("Nina")  # Another survivor
    survivor2.take_wound()  # Wound Nina
    survivor2.take_wound()  # Kill Nina
    assert game.history.count("The game has ended: all survivors died") == 0  # Game still not over

    assert game.history == [
        "Game started at 2026-01-01T12:00:00",
        "Jack joined the game",
        "Jack acquired Baseball Bat",
        "Jack was wounded",
        "Jack died",
        "Liam joined the game",
        "Mona joined the game",
        "Nina joined the game",
        "Nina was wounded",
        "Nina died",
    ]  # Complete history

    survivor3 = game.add_survivor("Owen")  # Add another survivor
    survivor3.take_wound()  # Wound Owen
    assert game.history[-1] == "Owen was wounded"  # History updated

    # Test for a non-level-changing kill announces nothing
    survivor.kill_zombie()  # A kill that does not change level
    assert game.history.count("Owen advanced to") == 0  # No announcement for non-level-change
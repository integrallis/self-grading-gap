import pytest
from solution import compute_door_states

# US-1: Compute the final door states
def test_one_door_opens():
    # With 1 door, it toggles once and ends open.
    assert compute_door_states(1) == (["@"], [1], "@")

def test_two_doors():
    # 1st door toggled once (open), 2nd door toggled twice (closed).
    assert compute_door_states(2) == (["@", "#"], [1], "@#")

def test_ten_doors():
    # Doors at positions 1, 4, 9 remain open after 10 toggles.
    assert compute_door_states(10) == (["@", "#", "#", "@", "#", "#", "#", "#", "@", "#"], [1, 4, 9], "@##@####@#")

def test_one_hundred_doors():
    # Doors at positions 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 remain open after 100 toggles.
    assert compute_door_states(100) == (["@", "#", "#", "@", "#", "#", "#", "#", "@", "#"] + ["#"] * 90,
                                         [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
                                         "@##@####@##################################################")

def test_zero_doors():
    # With 0 doors, all outputs should be empty.
    assert compute_door_states(0) == ([], [], "")

# US-3: Handle edge counts
def test_negative_doors():
    # Negative door count should raise an error with the specified message.
    with pytest.raises(ValueError, match="door count must be non-negative"):
        compute_door_states(-1)
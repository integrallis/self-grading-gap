from solution import Calculator

def test_seeding_sets_starting_value():
    calc = Calculator()
    calc.seed(10)
    result = calc.result()  # Expect 10
    assert result == 10

def test_addition_increases_running_value():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    result = calc.result()  # Expect 15 (10 + 5)
    assert result == 15

def test_addition_chains_and_accumulates():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).add(5)
    result = calc.result()  # Expect 20 (10 + 5 + 5)
    assert result == 20

def test_subtraction_decreases_running_value():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(3)
    result = calc.result()  # Expect 7 (10 - 3)
    assert result == 7

def test_addition_and_subtraction_combine():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(3)
    result = calc.result()  # Expect 12 (10 + 5 - 3)
    assert result == 12

def test_chain_returns_same_calculator():
    calc = Calculator()
    result = calc.seed(10).add(5).subtract(3)  # Should return the same calculator instance
    assert result is calc

def test_invalid_seed_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.seed(20)  # Ignored
    result = calc.result()  # Expect 10
    assert result == 10

def test_invalid_addition_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.add('five')  # Ignored
    result = calc.result()  # Expect 10
    assert result == 10

def test_unseeded_calculator_reports_zero():
    calc = Calculator()
    result = calc.result()  # Expect 0
    assert result == 0

def test_negative_seed_is_valid():
    calc = Calculator()
    calc.seed(-5)
    result = calc.result()  # Expect -5
    assert result == -5

def test_undo_reverts_last_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    result = calc.result()  # Expect 10
    assert result == 10

def test_multiple_undos_step_back_through_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.subtract(3)
    calc.undo()  # Undo subtract
    result = calc.result()  # Expect 15 (10 + 5)
    assert result == 15
    calc.undo()  # Undo add
    result = calc.result()  # Expect 10
    assert result == 10

def test_undo_does_not_undo_past_seed():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.undo()  # No effect, should still be at seed
    result = calc.result()  # Expect 10
    assert result == 10

def test_undo_on_unseeded_calculator_changes_nothing():
    calc = Calculator()
    calc.undo()  # No effect
    result = calc.result()  # Expect 0
    assert result == 0

def test_redo_reapplies_last_undone_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.subtract(3)
    calc.undo()  # Undo subtract
    calc.redo()  # Redo subtract
    result = calc.result()  # Expect 12 (10 + 5 - 3)
    assert result == 12

def test_redo_with_nothing_undone_changes_nothing():
    calc = Calculator()
    calc.seed(10)
    calc.redo()  # No effect
    result = calc.result()  # Expect 10
    assert result == 10

def test_new_operation_after_undo_discards_redo_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()  # Undo add
    calc.add(3)  # New operation
    result = calc.result()  # Expect 13 (10 + 3)
    assert result == 13
    calc.redo()  # No effect
    assert calc.result() == 13

def test_redone_operation_can_be_undone_again():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.subtract(3)
    calc.undo()  # Undo subtract
    calc.redo()  # Redo subtract
    calc.undo()  # Undo again
    result = calc.result()  # Expect 15 (10 + 5)
    assert result == 15

def test_save_seals_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.save()  # Seal the history
    calc.undo()  # No effect
    result = calc.result()  # Expect 15
    assert result == 15

def test_new_operations_after_save_build_fresh_history():
    calc = Calculator()
    calc.seed(10)
    calc.save()  # Seal the history
    calc.add(5)  # New operation
    result = calc.result()  # Expect 15 (10 + 5)
    assert result == 15
    calc.undo()  # Should revert to 10
    assert calc.result() == 10
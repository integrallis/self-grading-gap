from solution import Calculator  # Assuming the class is named Calculator

def test_seeding_sets_starting_value():
    calc = Calculator()
    calc.seed(10)
    assert calc.result() == 10  # Seeded value should be reported

def test_chain_additions():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).add(5)
    assert calc.result() == 20  # 10 + 5 + 5 = 20

def test_chain_subtractions():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(5).subtract(2)
    assert calc.result() == 3  # 10 - 5 - 2 = 3

def test_chain_additions_and_subtractions():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2).add(3)
    assert calc.result() == 16  # 10 + 5 - 2 + 3 = 16

def test_chaining_methods():
    calc = Calculator()
    result = calc.seed(10).add(5).subtract(2)
    assert result is calc  # Should return the same calculator instance

def test_invalid_seed_ignored():
    calc = Calculator()
    calc.seed("invalid")  # Invalid seed, should be ignored
    calc.seed(10)  # Valid seed
    assert calc.result() == 10  # Should be 10

def test_invalid_addition_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.add("invalid")  # Invalid input, should be ignored
    assert calc.result() == 10  # Still should be 10

def test_invalid_subtraction_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(3.5)  # Invalid input, should be ignored
    assert calc.result() == 10  # Still should be 10

def test_unseeded_calculator_reports_zero():
    calc = Calculator()
    assert calc.result() == 0  # Should report 0 without raising

def test_negative_seed_is_valid():
    calc = Calculator()
    calc.seed(-5)
    assert calc.result() == -5  # Seeded value should be reported

def test_negative_operand_addition():
    calc = Calculator()
    calc.seed(10)
    calc.add(-3)  # Valid operation
    assert calc.result() == 7  # 10 + (-3) = 7

def test_negative_operand_subtraction():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(-2)  # Valid operation
    assert calc.result() == 12  # 10 - (-2) = 12

def test_undo_reverts_last_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2)
    calc.undo()
    assert calc.result() == 15  # Last operation was subtract(2), now reverted

def test_repeated_undo_steps_back():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2)
    calc.undo()
    calc.undo()
    assert calc.result() == 10  # Reverted both operations, should be back to seed

def test_undo_does_not_revert_past_seed():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.undo()  # Should do nothing as there's nothing to revert to before seed
    assert calc.result() == 10  # Remains at seed value

def test_undo_on_unseeded_changes_nothing():
    calc = Calculator()
    calc.undo()  # Should do nothing
    assert calc.result() == 0  # Reports 0

def test_redo_reapplies_last_undone_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2)
    calc.undo()
    calc.undo()
    calc.redo()
    assert calc.result() == 15  # Should reapply the last operation after two undos

def test_redo_with_nothing_to_redo_changes_nothing():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.redo()
    calc.redo()  # Should do nothing
    assert calc.result() == 15  # Should still be the last valid state

def test_new_operation_after_undo_discards_redo_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.add(3)  # New operation after undo
    assert calc.result() == 13  # Should only reflect new operation

def test_redoing_a_redone_operation_can_be_undone():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.redo()
    calc.undo()  # Undo again
    assert calc.result() == 10  # Should revert back to seed

def test_save_seals_the_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.save()  # Seals the state
    calc.undo()  # Should do nothing after save
    assert calc.result() == 15  # Should still be 15

def test_new_operations_after_save_are_accepted():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.save()  # Seals the state
    calc.add(3)  # New operation
    assert calc.result() == 18  # Should reflect new operation after save

def test_undo_after_save_changes_nothing():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.save()  # Seals the state
    calc.undo()  # Should do nothing
    assert calc.result() == 15  # Should still be 15

def test_redo_after_save_changes_nothing():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.save()  # Seals the state
    calc.undo()  # Undo last operation
    calc.redo()  # Should do nothing
    assert calc.result() == 15  # Should still be 15

def test_second_seed_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.seed(20)  # This seed should be ignored
    assert calc.result() == 10  # Should be 10

def test_operations_before_seeding_ignored():
    calc = Calculator()
    calc.add(5)  # Ignored, not seeded
    calc.subtract(3)  # Ignored, not seeded
    calc.seed(10)
    assert calc.result() == 10  # Should be 10 after seeding

def test_fractional_seed_ignored():
    calc = Calculator()
    calc.seed(3.14)  # Invalid seed, should be ignored
    calc.seed(10)  # Valid seed
    assert calc.result() == 10  # Should be 10

def test_add_fractional_operand_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.add(2.5)  # Invalid input, should be ignored
    assert calc.result() == 10  # Still should be 10

def test_subtract_text_operand_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.subtract("invalid")  # Invalid input, should be ignored
    assert calc.result() == 10  # Still should be 10
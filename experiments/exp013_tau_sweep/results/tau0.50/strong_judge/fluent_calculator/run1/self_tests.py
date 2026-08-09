from solution import Calculator

def test_seeding_calculator_sets_starting_value():
    calc = Calculator()
    calc.seed(10)
    assert calc.result() == 10  # Expected: 10 (initial seed value)

def test_chaining_additions():
    calc = Calculator()
    calc.seed(10).add(5).add(5)
    assert calc.result() == 20  # Expected: 10 + 5 + 5 = 20

def test_chaining_subtractions():
    calc = Calculator()
    calc.seed(10).subtract(3).subtract(2)
    assert calc.result() == 5  # Expected: 10 - 3 - 2 = 5

def test_combining_additions_and_subtractions():
    calc = Calculator()
    calc.seed(10).add(5).subtract(3)
    assert calc.result() == 12  # Expected: 10 + 5 - 3 = 12

def test_chain_returns_self():
    calc = Calculator()
    assert calc.seed(10) is calc  # Should return itself
    assert calc.add(5) is calc    # Should return itself
    assert calc.subtract(3) is calc  # Should return itself
    assert calc.undo() is calc     # Should return itself
    assert calc.redo() is calc     # Should return itself
    assert calc.save() is calc     # Should return itself

def test_invalid_second_seed_is_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.seed(20)
    assert calc.result() == 10  # Expected: 10 (the first seed is what counts)

def test_additions_before_seeding_are_ignored():
    calc = Calculator()
    calc.add(5)
    calc.seed(10)
    assert calc.result() == 10  # Expected: 10 (additions before seeding are ignored)

def test_subtractions_before_seeding_are_ignored():
    calc = Calculator()
    calc.subtract(5)
    calc.seed(10)
    assert calc.result() == 10  # Expected: 10 (subtractions before seeding are ignored)

def test_result_of_unseeded_calculator_is_zero():
    calc = Calculator()
    assert calc.result() == 0  # Expected: 0 (unseeded calculator)

def test_invalid_non_whole_number_operand_is_ignored():
    calc = Calculator()
    calc.seed(10).add(5.5)
    assert calc.result() == 10  # Expected: 10 (non-whole addition is ignored)

def test_invalid_subtraction_operand_is_ignored():
    calc = Calculator()
    calc.seed(10).subtract(1.5)
    assert calc.result() == 10  # Expected: 10 (invalid subtraction is ignored)

def test_invalid_text_operand_is_ignored():
    calc = Calculator()
    calc.seed(10).add("x").subtract("x")
    assert calc.result() == 10  # Expected: 10 (invalid operands are ignored)

def test_valid_negative_seed():
    calc = Calculator()
    calc.seed(-5)
    assert calc.result() == -5  # Expected: -5 (negative seed is valid)

def test_negative_operand():
    calc = Calculator()
    calc.seed(10).add(-3).subtract(-2)
    assert calc.result() == 9  # Expected: 10 + (-3) + 2 = 9

def test_undo_reverts_last_operation():
    calc = Calculator()
    calc.seed(10).add(5).undo()
    assert calc.result() == 10  # Expected: 10 (undoing the last addition)

def test_undo_reverts_subtraction():
    calc = Calculator()
    calc.seed(10).subtract(3).undo()
    assert calc.result() == 10  # Expected: 10 (undoing the last subtraction)

def test_multiple_undos():
    calc = Calculator()
    calc.seed(10).add(5).subtract(2).undo().undo()
    assert calc.result() == 10  # Expected: 10 (two undos revert to the seed)

def test_undo_does_not_revert_past_seed():
    calc = Calculator()
    calc.seed(10).undo().undo()
    assert calc.result() == 10  # Expected: 10 (no change if no operations)

def test_undo_on_unseeded_calculator_changes_nothing():
    calc = Calculator()
    calc.undo()
    assert calc.result() == 0  # Expected: 0 (no operation to undo)

def test_redo_reapplies_last_undone_operation():
    calc = Calculator()
    calc.seed(10).add(5).undo().redo()
    assert calc.result() == 15  # Expected: 15 (redoing the last addition)

def test_redo_with_nothing_undone_changes_nothing():
    calc = Calculator()
    calc.seed(10).add(5)
    calc.redo()  # No undo yet
    assert calc.result() == 15  # Expected: 15 (no change)

def test_new_operation_after_undo_discards_redo_history():
    calc = Calculator()
    calc.seed(10).add(5).undo().add(2)
    assert calc.result() == 12  # Expected: 12 (new operation after undo)

def test_redo_on_redone_operation_can_be_undone():
    calc = Calculator()
    calc.seed(10).add(5).undo().redo().undo()
    assert calc.result() == 10  # Expected: 10 (undoing the redone addition)

def test_save_seals_the_history():
    calc = Calculator()
    calc.seed(10).add(5).save()
    calc.undo()
    assert calc.result() == 15  # Expected: 15 (undo has no effect after save)

def test_new_operations_after_save_are_accepted():
    calc = Calculator()
    calc.seed(10).add(5).save().add(2)
    assert calc.result() == 17  # Expected: 17 (new operation after save)

def test_save_with_pending_redo_history():
    calc = Calculator()
    calc.seed(10).add(5).subtract(2).undo().save().redo()
    assert calc.result() == 15  # Expected: 15 (redo has no effect after save)

def test_invalid_seed_ignored_and_later_valid_seed_applies():
    calc = Calculator()
    calc.seed(1.5).seed(10)
    assert calc.result() == 10  # Expected: 10 (invalid seed is ignored)

def test_undo_on_unseeded_calculator_with_later_seed():
    calc = Calculator()
    calc.undo()
    calc.seed(10)
    assert calc.result() == 10  # Expected: 10 (later valid seed applies)
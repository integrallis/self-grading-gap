from solution import Calculator

def test_seeding_sets_starting_value():
    calculator = Calculator()
    calculator.seed(10)
    assert calculator.result() == 10  # AC-1.1

def test_chaining_additions():
    calculator = Calculator()
    calculator.seed(10).add(5).add(5)
    assert calculator.result() == 20  # AC-1.2

def test_chaining_subtractions():
    calculator = Calculator()
    calculator.seed(10).subtract(3)
    assert calculator.result() == 7  # AC-1.3

def test_chaining_additions_and_subtractions():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(3)
    assert calculator.result() == 12  # AC-1.4

def test_chainable_calls():
    calculator = Calculator()
    result = calculator.seed(10).add(5)
    assert result is calculator  # AC-1.5
    result = calculator.subtract(3)
    assert result is calculator  # AC-1.5
    result = calculator.undo()
    assert result is calculator  # AC-1.5
    result = calculator.redo()
    assert result is calculator  # AC-1.5
    result = calculator.save()
    assert result is calculator  # AC-1.5

def test_ignore_second_seed():
    calculator = Calculator()
    calculator.seed(10).seed(20)
    assert calculator.result() == 10  # AC-2.1

def test_ignore_operations_before_seeding():
    calculator = Calculator()
    calculator.add(5)
    calculator.subtract(3)
    calculator.seed(10)
    assert calculator.result() == 10  # AC-2.2

def test_result_of_unseeded_calculator():
    calculator = Calculator()
    assert calculator.result() == 0  # AC-2.3

def test_ignore_non_whole_number_addition():
    calculator = Calculator()
    calculator.seed(10).add(5.5)
    assert calculator.result() == 10  # AC-2.4

def test_ignore_non_whole_number_subtraction():
    calculator = Calculator()
    calculator.seed(10).subtract(1.5)
    assert calculator.result() == 10  # AC-2.4

def test_ignore_non_whole_number_seed():
    calculator = Calculator()
    calculator.seed(5.5).seed(10)
    assert calculator.result() == 10  # AC-2.5

def test_negative_number_operations():
    calculator = Calculator()
    calculator.seed(-10).add(-5).subtract(-2)
    assert calculator.result() == -13  # AC-2.6

def test_undo_single_operation():
    calculator = Calculator()
    calculator.seed(10).add(5).undo()
    assert calculator.result() == 10  # AC-3.1

def test_undo_multiple_operations():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(2).undo().undo()
    assert calculator.result() == 10  # AC-3.2

def test_undo_does_not_revert_past_seed():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(2).undo().undo()
    assert calculator.result() == 10  # AC-3.3

def test_undo_on_unseeded_calculator():
    calculator = Calculator()
    calculator.undo()
    calculator.seed(10)
    assert calculator.result() == 10  # AC-3.4

def test_redo_single_operation():
    calculator = Calculator()
    calculator.seed(10).add(5).undo().redo()
    assert calculator.result() == 15  # AC-4.1

def test_redo_with_no_operations():
    calculator = Calculator()
    calculator.seed(10).redo()
    assert calculator.result() == 10  # AC-4.2

def test_new_operation_after_undo_discards_redo():
    calculator = Calculator()
    calculator.seed(10).add(5).undo().add(2).redo()
    assert calculator.result() == 12  # AC-4.3

def test_redone_operation_can_be_undone():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(2).undo().redo().undo()
    assert calculator.result() == 10  # AC-4.4

def test_save_seals_history():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(2).undo().save()
    calculator.undo()
    assert calculator.result() == 15  # AC-5.1

def test_new_operations_after_save():
    calculator = Calculator()
    calculator.seed(10).add(5).save().add(2)
    assert calculator.result() == 17  # AC-5.2

def test_save_with_pending_redo():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(2).undo().save()
    assert calculator.result() == 15  # AC-5.1
    calculator.undo()
    assert calculator.result() == 15  # AC-5.1
    calculator.redo()
    assert calculator.result() == 15  # AC-5.1

def test_ignore_invalid_addition_with_text():
    calculator = Calculator()
    calculator.seed(10).add("five")
    assert calculator.result() == 10  # AC-2.4

def test_ignore_invalid_subtraction_with_text():
    calculator = Calculator()
    calculator.seed(10).subtract("five")
    assert calculator.result() == 10  # AC-2.4

def test_exhausted_undo_history():
    calculator = Calculator()
    calculator.seed(10).add(5).undo().undo()
    assert calculator.result() == 10  # AC-3.3

def test_redo_order():
    calculator = Calculator()
    calculator.seed(10).add(5).subtract(2).undo().undo().redo()
    assert calculator.result() == 15  # AC-4.1

def test_post_save_fresh_history():
    calculator = Calculator()
    calculator.seed(10).add(5).save().add(2).undo()
    assert calculator.result() == 17  # AC-5.2
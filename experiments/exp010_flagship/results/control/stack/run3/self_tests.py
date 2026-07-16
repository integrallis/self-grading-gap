import pytest
from solution import BoundedStack  # Assuming the class name for the stack is BoundedStack

def test_new_stack_is_empty():
    stack = BoundedStack()
    # A newly created stack is empty
    assert stack.is_empty() is True

def test_pushing_one_value_leaves_stack_empty_after_pop():
    stack = BoundedStack()
    stack.push(1)
    stack.pop()
    # Pushing one value and popping it leaves the stack empty
    assert stack.is_empty() is True

def test_pushing_two_values_and_popping_one_leaves_stack_non_empty():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.pop()
    # Pushing two values and popping one leaves it non-empty
    assert stack.is_empty() is False

def test_popping_returns_values_in_reverse_order():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    value1 = stack.pop()  # Should be 2
    value2 = stack.pop()  # Should be 1
    # Popping returns values in the reverse of the order they were pushed
    assert value1 == 2
    assert value2 == 1

def test_popping_empty_stack_fails_with_dedicated_error():
    stack = BoundedStack()
    with pytest.raises(Exception) as excinfo:
        stack.pop()
    # Popping an empty stack fails with a dedicated empty-stack error
    assert str(excinfo.value) == "Cannot pop from empty stack"

def test_full_stack_error_message():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)  # Assuming stack allows only 2 items for this test
    with pytest.raises(Exception) as excinfo:
        stack.push(4)
    # The full-stack failure message is exactly "Stack is full"
    assert str(excinfo.value) == "Stack is full"

def test_capacity_of_zero_results_in_full_stack_on_first_push():
    stack = BoundedStack(0)
    with pytest.raises(Exception) as excinfo:
        stack.push(1)
    # A capacity of zero is valid — the very first push already fails as full
    assert str(excinfo.value) == "Stack is full"

def test_negative_capacity_rejected_at_creation():
    with pytest.raises(Exception) as excinfo:
        BoundedStack(-1)
    # A negative capacity is rejected at creation with the exact message "Capacity cannot be negative"
    assert str(excinfo.value) == "Capacity cannot be negative"
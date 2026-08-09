import pytest
from solution import BoundedStack

def test_newly_created_stack_is_empty():
    stack = BoundedStack()
    assert stack.is_empty()  # AC-1.1: A newly created stack is empty.

def test_pushing_and_popping_leaves_stack_empty():
    stack = BoundedStack()
    stack.push(1)
    stack.pop()
    assert stack.is_empty()  # AC-1.2: Emptiness tracks contents.

def test_pushing_two_values_and_popping_one_leaves_stack_non_empty():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.pop()
    assert not stack.is_empty()  # AC-1.2: Emptiness tracks contents.

def test_pop_returns_values_in_reverse_order():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    popped_value_1 = stack.pop()
    assert popped_value_1 == 2  # AC-1.3: Popping returns values in reverse order.
    popped_value_2 = stack.pop()
    assert popped_value_2 == 1  # AC-1.3: Popping returns values in reverse order.

def test_popping_empty_stack_fails_with_empty_stack_error():
    stack = BoundedStack()
    with pytest.raises(Exception) as excinfo:
        stack.pop()
    assert str(excinfo.value) == "Cannot pop from empty stack"  # AC-2.1 and AC-2.2

def test_push_on_full_stack_fails_with_full_stack_error():
    stack = BoundedStack(max_capacity=1)
    stack.push(1)
    with pytest.raises(Exception) as excinfo:
        stack.push(2)
    assert str(excinfo.value) == "Stack is full"  # AC-3.1 and AC-3.2

def test_capacity_zero_prevents_first_push():
    stack = BoundedStack(max_capacity=0)
    with pytest.raises(Exception) as excinfo:
        stack.push(1)
    assert str(excinfo.value) == "Stack is full"  # AC-3.3

def test_negative_capacity_rejected_at_creation():
    with pytest.raises(Exception) as excinfo:
        BoundedStack(max_capacity=-1)
    assert str(excinfo.value) == "Capacity cannot be negative"  # AC-3.4

def test_pop_from_full_stack_and_push_succeeds():
    stack = BoundedStack(max_capacity=1)
    stack.push(1)
    stack.pop()  # Now the stack is empty
    stack.push(2)  # This should succeed
    assert not stack.is_empty()  # The stack should have one item now
    assert stack.pop() == 2  # Popping should return the last pushed value
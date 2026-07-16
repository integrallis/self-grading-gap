# test_bounded_stack.py

import pytest
from solution import stack  # The public API will be imported from the solution package

def test_new_stack_is_empty():
    s = stack()  # Creating a new stack
    assert s.is_empty()  # AC-1.1: A newly created stack is empty

def test_push_and_pop_empty_stack():
    s = stack()  # Creating a new stack
    s.push(1)
    s.pop()
    assert s.is_empty()  # AC-1.2: Emptiness tracks contents

def test_push_two_pop_one_stack_non_empty():
    s = stack()  # Creating a new stack
    s.push(1)
    s.push(2)
    s.pop()
    assert not s.is_empty()  # AC-1.2: Pushing two values and popping one leaves it non-empty

def test_pop_returns_values_in_reverse_order():
    s = stack()  # Creating a new stack
    s.push(1)  # First pushed
    s.push(2)  # Second pushed
    assert s.pop() == 2  # AC-1.3: Popping returns values in reverse order
    assert s.pop() == 1

def test_pop_empty_stack_fails():
    s = stack()  # Creating a new stack
    with pytest.raises(Exception) as excinfo:  # AC-2.1: Popping an empty stack fails
        s.pop()
    assert str(excinfo.value) == "Cannot pop from empty stack"  # AC-2.2: Exact failure message

def test_push_full_stack_fails():
    s = stack(2)  # Creating with a capacity of 2
    s.push(1)
    s.push(2)
    with pytest.raises(Exception) as excinfo:  # AC-3.1: Pushing onto a full stack fails
        s.push(3)
    assert str(excinfo.value) == "Stack is full"  # AC-3.2: Exact full stack message

    # Verify that the rejected value was not added
    assert s.pop() == 2  # Should return the last pushed value
    assert s.pop() == 1  # Should return the first pushed value
    assert s.is_empty()  # Stack should be empty after popping all values

def test_capacity_zero_fails_first_push():
    s = stack(0)  # Creating with a capacity of 0
    with pytest.raises(Exception) as excinfo:  # AC-3.3: First push fails as full
        s.push(1)
    assert str(excinfo.value) == "Stack is full"  # AC-3.2: Exact full stack message

def test_negative_capacity_rejected():
    with pytest.raises(Exception) as excinfo:  # AC-3.4: Negative capacity is rejected
        stack(-1)
    assert str(excinfo.value) == "Capacity cannot be negative"  # Exact rejection message

def test_empty_and_full_exceptions_are_distinct():
    s = stack(2)  # Creating with a capacity of 2
    with pytest.raises(Exception) as excinfo_full:  # Test full stack exception
        s.push(1)
        s.push(2)
        s.push(3)
    with pytest.raises(Exception) as excinfo_empty:  # Test empty stack exception
        s.pop()
        s.pop()
        s.pop()
    assert str(excinfo_full.value) == "Stack is full"  # AC-3.2: Exact full stack message
    assert str(excinfo_empty.value) == "Cannot pop from empty stack"  # AC-2.2: Exact empty stack message
    assert excinfo_full.value != excinfo_empty.value  # Ensure the exceptions are distinct
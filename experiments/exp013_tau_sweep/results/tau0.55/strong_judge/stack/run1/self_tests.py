import pytest
from solution import BoundedStack  # Assuming BoundedStack is the class defined in the solution package

def test_initially_empty_stack():
    stack = BoundedStack()
    assert stack.is_empty()  # AC-1.1: A newly created stack is empty

def test_stack_emptiness_tracks_contents():
    stack = BoundedStack()
    stack.push(1)
    assert not stack.is_empty()  # After pushing one value, stack is not empty
    stack.pop()
    assert stack.is_empty()  # After popping, stack is empty again

    stack.push(1)
    stack.push(2)
    assert not stack.is_empty()  # After pushing two values, stack is not empty
    stack.pop()
    assert not stack.is_empty()  # After popping one, stack is still not empty
    stack.pop()
    assert stack.is_empty()  # After popping all, stack is empty again

def test_stack_pops_in_reverse_order():
    stack = BoundedStack()
    stack.push(1)  # Push 1
    stack.push(2)  # Push 2
    assert stack.pop() == 2  # Popping should return 2 (most recently added)
    assert stack.pop() == 1  # Popping should return 1 next

def test_popping_empty_stack_fails():
    stack = BoundedStack()
    with pytest.raises(Exception) as exc_info:  # AC-2.1: Popping an empty stack fails
        stack.pop()
    assert str(exc_info.value) == "Cannot pop from empty stack"  # AC-2.2: Failure message

def test_push_on_full_stack_fails():
    stack = BoundedStack(capacity=1)  # AC-3.1: Setting capacity at creation
    stack.push(1)
    with pytest.raises(Exception) as exc_info:  # Pushing onto a full stack fails
        stack.push(2)
    assert str(exc_info.value) == "Stack is full"  # AC-3.2: Failure message

def test_zero_capacity_stack():
    stack = BoundedStack(capacity=0)  # AC-3.3: Capacity of zero
    with pytest.raises(Exception) as exc_info:  # First push fails
        stack.push(1)
    assert str(exc_info.value) == "Stack is full"  # Failure message

def test_negative_capacity_rejected():
    with pytest.raises(Exception) as exc_info:  # AC-3.4: Negative capacity is rejected
        BoundedStack(capacity=-1)
    assert str(exc_info.value) == "Capacity cannot be negative"  # Failure message

def test_empty_pop_and_full_push_failures_are_distinct():
    empty_stack = BoundedStack()
    full_stack = BoundedStack(capacity=1)
    full_stack.push(1)
    
    with pytest.raises(Exception) as empty_exc_info:
        empty_stack.pop()
    with pytest.raises(Exception) as full_exc_info:
        full_stack.push(2)

    assert str(empty_exc_info.value) == "Cannot pop from empty stack"
    assert str(full_exc_info.value) == "Stack is full"
    assert empty_exc_info.value is not full_exc_info.value  # Ensure they are distinct exceptions

def test_capacity_recovery():
    stack = BoundedStack(capacity=1)
    stack.push(1)
    with pytest.raises(Exception) as exc_info:  # Pushing onto a full stack fails
        stack.push(2)
    assert str(exc_info.value) == "Stack is full"  # Confirm full stack failure message

    stack.pop()  # Pop the value
    stack.push(2)  # Now this push should succeed
    assert stack.pop() == 2  # Popping should return 2
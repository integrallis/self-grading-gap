from solution import BoundedStack

def test_newly_created_stack_is_empty():
    stack = BoundedStack()
    assert stack.is_empty()  # AC-1.1: A newly created stack is empty.

def test_emptiness_tracks_contents():
    stack = BoundedStack()
    stack.push(1)  # Push one value
    assert not stack.is_empty()  # After pushing, stack should not be empty
    stack.pop()  # Pop the value
    assert stack.is_empty()  # After popping, stack should be empty

    stack.push(1)  # Push one value
    stack.push(2)  # Push another value
    assert not stack.is_empty()  # After pushing two values, should not be empty
    stack.pop()  # Pop one value
    assert not stack.is_empty()  # Should still be non-empty after one pop

def test_popping_returns_values_in_reverse_order():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    
    assert stack.pop() == 3  # Last pushed value is returned first (AC-1.3)
    assert stack.pop() == 2  # Next value
    assert stack.pop() == 1  # Finally, the first value

def test_popping_empty_stack_fails():
    stack = BoundedStack()
    try:
        stack.pop()  # Attempt to pop from empty stack
    except Exception as e:
        assert str(e) == "Cannot pop from empty stack"  # AC-2.1 and AC-2.2

def test_pushing_to_full_stack_fails():
    stack = BoundedStack(2)  # Set max capacity to 2
    stack.push(1)
    stack.push(2)
    try:
        stack.push(3)  # Attempt to push beyond capacity
    except Exception as e:
        assert str(e) == "Stack is full"  # AC-3.1 and AC-3.2

def test_capacity_zero():
    stack = BoundedStack(0)  # Create stack with zero capacity
    try:
        stack.push(1)  # Attempt to push should fail
    except Exception as e:
        assert str(e) == "Stack is full"  # AC-3.3

def test_negative_capacity_rejected():
    try:
        stack = BoundedStack(-1)  # Attempt to create with negative capacity
    except Exception as e:
        assert str(e) == "Capacity cannot be negative"  # AC-3.4
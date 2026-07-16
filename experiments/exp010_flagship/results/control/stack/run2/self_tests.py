from solution import BoundedStack

def test_new_stack_is_empty():
    # A newly created stack is empty.
    stack = BoundedStack()
    assert stack.is_empty()  # Expect True

def test_pushing_and_popping():
    # Pushing one value and popping it leaves the stack empty.
    stack = BoundedStack()
    stack.push(1)
    assert not stack.is_empty()  # Expect False
    stack.pop()
    assert stack.is_empty()  # Expect True

    # Pushing two values and popping one leaves it non-empty.
    stack.push(1)
    stack.push(2)
    stack.pop()
    assert not stack.is_empty()  # Expect False

def test_popping_returns_values_in_reverse_order():
    # Popping returns values in the reverse of the order they were pushed.
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2  # Expect 2
    assert stack.pop() == 1  # Expect 1

def test_popping_empty_stack_fails():
    # Popping an empty stack fails with a dedicated empty-stack error.
    stack = BoundedStack()
    try:
        stack.pop()
        assert False  # Expecting an exception, should not reach here
    except Exception as e:
        assert str(e) == "Cannot pop from empty stack"  # Exact message

def test_capacity_of_zero():
    # A capacity of zero is valid — the very first push already fails as full.
    stack = BoundedStack(0)
    try:
        stack.push(1)
        assert False  # Expecting an exception, should not reach here
    except Exception as e:
        assert str(e) == "Stack is full"  # Exact message

def test_negative_capacity_rejected_at_creation():
    # A negative capacity is rejected at creation with the exact message.
    try:
        BoundedStack(-1)
        assert False  # Expecting an exception, should not reach here
    except Exception as e:
        assert str(e) == "Capacity cannot be negative"  # Exact message

def test_pushing_exceeding_capacity_fails():
    # A maximum capacity may be set at creation; pushing onto a full stack fails.
    stack = BoundedStack(1)
    stack.push(1)
    try:
        stack.push(2)
        assert False  # Expecting an exception, should not reach here
    except Exception as e:
        assert str(e) == "Stack is full"  # Exact message
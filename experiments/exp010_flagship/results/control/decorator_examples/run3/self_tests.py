from solution import register_function, active_functions

def test_decorated_function_carries_activation_status():
    @register_function
    def sample_function():
        pass
    assert hasattr(sample_function, 'status')  # AC-1.1
    assert sample_function.status == "active"  # AC-1.2

def test_decorated_function_inactive_status():
    @register_function(active=False)
    def inactive_function():
        pass
    assert hasattr(inactive_function, 'status')  # AC-1.1
    assert inactive_function.status == "inactive"  # AC-1.3

def test_status_values_are_exact():
    @register_function
    def another_function():
        pass
    assert another_function.status == "active"  # AC-1.2
    @register_function(active=False)
    def yet_another_function():
        pass
    assert yet_another_function.status == "inactive"  # AC-1.3

def test_active_function_added_to_registry():
    @register_function
    def active_function():
        pass
    assert active_function in active_functions  # AC-2.1

def test_inactive_function_not_added_to_registry():
    @register_function(active=False)
    def inactive_function():
        pass
    assert inactive_function not in active_functions  # AC-2.2

def test_registry_contains_function_objects():
    @register_function
    def another_active_function():
        pass
    assert another_active_function in active_functions  # AC-2.1
    assert len(active_functions) == 1  # Ensure only one function is present

def test_decorated_function_unchanged():
    @register_function
    def unchanged_function():
        return 42
    # No assertion for return value as it is not specified

def test_sample_subjects_behavior():
    @register_function
    def sample_active():
        pass
    
    @register_function(active=False)
    def sample_inactive():
        pass
    
    @register_function
    def sample_active_two():
        pass
    
    assert sample_active in active_functions  # AC-3.1
    assert sample_inactive not in active_functions  # AC-3.2
    assert sample_active in active_functions  # Re-check for sample_active
    assert sample_active_two in active_functions  # AC-3.3
    assert len(active_functions) == 2  # Only two active functions
    assert sample_active() is None  # AC-3.4
    assert sample_inactive() is None  # AC-3.4
    assert sample_active_two() is None  # AC-3.4
    assert sample_active.status == "active"  # AC-3.5
    assert sample_inactive.status == "inactive"  # AC-3.5
    assert sample_active_two.status == "active"  # AC-3.5

def test_result_conversion_to_string():
    @register_function
    def add(a, b):
        return a + b

    @register_function
    def multiply(a, b):
        return a * b

    add_result = add(5, 6)  # 5 + 6 = 11
    multiply_result = multiply(5, 6)  # 5 * 6 = 30

    assert isinstance(add_result, str)  # AC-4.1
    assert add_result == "11"  # AC-4.2
    assert isinstance(multiply_result, str)  # AC-4.1
    assert multiply_result == "30"  # AC-4.2

    # Test for metadata preservation
    assert add.__name__ == 'add'  # AC-4.4
    assert multiply.__name__ == 'multiply'  # AC-4.4
from solution import register_function, active_functions, convert_to_string

def test_decorated_function_carries_activation_status():
    @register_function
    def example_active_function():
        pass

    assert hasattr(example_active_function, 'status')
    assert isinstance(example_active_function.status, str)  # Check type
    assert example_active_function.status == "active"  # Default status

def test_decorated_function_inactive_status():
    @register_function(active=False)
    def example_inactive_function():
        pass

    assert hasattr(example_inactive_function, 'status')
    assert isinstance(example_inactive_function.status, str)  # Check type
    assert example_inactive_function.status == "inactive"  # Status for inactive

def test_active_function_added_to_registry():
    @register_function
    def example_function():
        pass

    assert example_function in active_functions  # Active function should be in the registry

def test_inactive_function_not_in_registry():
    @register_function(active=False)
    def example_function():
        pass

    assert example_function not in active_functions  # Inactive function should not be in the registry

def test_decoration_returns_same_function_object():
    def example_function():
        pass

    decorated_function = register_function(example_function)
    assert decorated_function is example_function  # Decoration should return the same function object

def test_decorated_function_is_callable():
    @register_function
    def example_function():
        return "I'm callable"

    assert example_function() == "I'm callable"  # Function remains callable

def test_sample_registry_contains_correct_functions():
    from solution import sample_active_function, sample_inactive_function, sample_active_function_2

    assert sample_active_function in active_functions  # First sample subject is active
    assert sample_inactive_function not in active_functions  # Second sample subject is inactive
    assert sample_active_function_2 in active_functions  # Third sample subject is active
    assert len(active_functions) == 2  # Should only contain first and third sample subjects

def test_sample_subjects_have_correct_status():
    from solution import sample_active_function, sample_inactive_function, sample_active_function_2

    assert sample_active_function.status == "active"  # Status for first sample
    assert sample_inactive_function.status == "inactive"  # Status for second sample
    assert sample_active_function_2.status == "active"  # Status for third sample

def test_call_all_sample_subjects():
    from solution import sample_active_function, sample_inactive_function, sample_active_function_2

    assert sample_active_function() is None  # First sample subject returns None
    assert sample_inactive_function() is None  # Second sample subject returns None
    assert sample_active_function_2() is None  # Third sample subject returns None

def test_convert_function_results_to_text():
    @convert_to_string
    @register_function
    def add_five_and_six():
        return 5 + 6

    @convert_to_string
    @register_function
    def multiply_five_and_six():
        return 5 * 6

    assert isinstance(add_five_and_six(), str)  # Should return a string
    assert add_five_and_six() == "11"  # 5 + 6 = 11
    assert isinstance(multiply_five_and_six(), str)  # Should return a string
    assert multiply_five_and_six() == "30"  # 5 * 6 = 30

def test_conversion_preserves_metadata():
    @convert_to_string
    @register_function
    def example_function():
        """This function adds numbers."""
        return 5 + 3

    assert example_function.__name__ == "example_function"  # Name should be preserved
    assert example_function.__doc__ == "This function adds numbers."  # Docstring should be preserved

def test_conversion_of_non_arithmetic_result():
    @convert_to_string
    @register_function
    def return_none():
        return None

    assert return_none() == "None"  # None should convert to "None"

def test_inactive_decorator_identity():
    def example_function():
        pass

    assert register_function(active=False)(example_function) is example_function  # Inactive decoration should return the same function object

def test_inactive_function_callability():
    @register_function(active=False)
    def example_function():
        return "I'm inactive"

    assert example_function() == "I'm inactive"  # Inactive function remains callable
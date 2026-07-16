# test_solution.py

from solution import registration_decorator, active_function, inactive_function, another_active_function

def test_active_function_status():
    assert active_function.status == "active"  # AC-1.2

def test_inactive_function_status():
    assert inactive_function.status == "inactive"  # AC-1.3

def test_another_active_function_status():
    assert another_active_function.status == "active"  # AC-1.2

def test_active_function_registration():
    assert active_function in registration_decorator.registered_functions  # AC-2.1

def test_inactive_function_registration():
    assert inactive_function not in registration_decorator.registered_functions  # AC-2.2

def test_another_active_function_registration():
    assert another_active_function in registration_decorator.registered_functions  # AC-2.1

def test_registered_functions_collection():
    assert registration_decorator.registered_functions == [active_function, another_active_function]  # AC-3.3

def test_active_function_callable():
    assert active_function() is None  # AC-3.4

def test_inactive_function_callable():
    assert inactive_function() is None  # AC-3.4

def test_another_active_function_callable():
    assert another_active_function() is None  # AC-3.4

def test_active_function_status_exact():
    assert active_function.status == "active"  # AC-1.4

def test_inactive_function_status_exact():
    assert inactive_function.status == "inactive"  # AC-1.4

def test_another_active_function_status_exact():
    assert another_active_function.status == "active"  # AC-1.4

def test_converted_function_string_return():
    result = registration_decorator.convert_to_string(active_function, 5, 6)  # Assuming this is the signature
    assert isinstance(result, str)  # AC-4.1

def test_converted_function_preserves_calculation():
    result = registration_decorator.convert_to_string(lambda x, y: x + y, 5, 6)
    assert result == "11"  # 5 + 6 = 11  # AC-4.2

def test_converted_function_preserves_calculation_multiplication():
    result = registration_decorator.convert_to_string(lambda x, y: x * y, 5, 6)
    assert result == "30"  # 5 * 6 = 30  # AC-4.2

def test_converted_function_keeps_name_metadata():
    wrapped_function = registration_decorator.convert_to_string(active_function, 5, 6)  # Assuming this is the signature
    assert wrapped_function.__name__ == active_function.__name__  # AC-4.4

def test_converted_function_keeps_description_metadata():
    wrapped_function = registration_decorator.convert_to_string(active_function, 5, 6)  # Assuming this is the signature
    assert wrapped_function.__doc__ == active_function.__doc__  # AC-4.4
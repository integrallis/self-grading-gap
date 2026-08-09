import pytest

def test_scaling_empty_recipe():
    # Scaling an empty recipe yields an empty recipe
    assert scale_recipe({}, 2) == {}

def test_scaling_recipe_with_factor_one():
    # A factor of one leaves every quantity unchanged
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    assert scale_recipe(original_recipe, 1) == original_recipe

def test_scaling_recipe_with_factor_zero():
    # A factor of zero zeroes every quantity
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    assert scale_recipe(original_recipe, 0) == {'sugar': 0.0, 'flour': 0.0}

def test_scaling_recipe_with_fractional_factor():
    # A factor of 0.5 halves quantities
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    assert scale_recipe(original_recipe, 0.5) == {'sugar': 0.5, 'flour': 1.0}

def test_scaling_recipe_with_large_factor():
    # A factor of 12 multiplies faithfully
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    assert scale_recipe(original_recipe, 12) == {'sugar': 12.0, 'flour': 24.0}

def test_scaling_recipe_with_fractional_quantities():
    # A factor of 1.5 scales quantities correctly
    original_recipe = {'ingredient': 1.5}
    assert scale_recipe(original_recipe, 1.5) == {'ingredient': 2.25}  # 1.5 * 1.5 = 2.25

def test_rounding_to_two_decimal_places_sugar():
    # Results are rounded to two decimal places by default
    original_recipe = {'sugar': 1/3}
    assert scale_recipe(original_recipe, 3) == {'sugar': 0.33}  # (1/3)*3 = 1.0, rounded to 0.33

def test_rounding_to_two_decimal_places_flour():
    # Results are rounded to two decimal places by default
    original_recipe = {'flour': 0.1}
    assert scale_recipe(original_recipe, 3) == {'flour': 0.30}  # 0.1*3 = 0.3

def test_rounding_with_custom_precision():
    # The rounding precision can be chosen explicitly
    original_recipe = {'sugar': 1/3}
    assert scale_recipe(original_recipe, 3, precision=4) == {'sugar': 0.3333}  # (1/3)*3 = 0.3333

def test_negative_scaling_factor():
    # A negative factor is rejected with an error
    original_recipe = {'sugar': 1.0}
    with pytest.raises(Exception, match="scaling factor must be non-negative"):
        scale_recipe(original_recipe, -1)

def test_zero_quantity_ingredient():
    # A zero quantity ingredient is rejected with an error
    original_recipe = {'sugar': 0.0}
    with pytest.raises(Exception, match=r"'sugar'.*must have a positive quantity|must have a positive quantity.*'sugar'"):
        scale_recipe(original_recipe, 1)

def test_negative_quantity_ingredient():
    # A negative quantity ingredient is rejected with an error
    original_recipe = {'sugar': -1.0}
    with pytest.raises(Exception, match=r"'sugar'.*must have a positive quantity|must have a positive quantity.*'sugar'"):
        scale_recipe(original_recipe, 1)

def test_preserving_original_recipe():
    # Scaling returns a new collection; the input recipe is left unmodified
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    scaled_recipe = scale_recipe(original_recipe, 2)
    assert scaled_recipe is not original_recipe  # They should not be the same object
    assert original_recipe == {'sugar': 1.0, 'flour': 2.0}  # Original must remain unchanged

def test_scaled_recipe_contains_original_ingredient_names():
    # The scaled recipe contains exactly the original ingredient names
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    scaled_recipe = scale_recipe(original_recipe, 2)
    assert set(scaled_recipe.keys()) == set(original_recipe.keys())  # They should have the same keys
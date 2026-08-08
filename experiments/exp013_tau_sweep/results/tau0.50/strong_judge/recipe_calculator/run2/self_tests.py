import pytest
from solution import scale_recipe  # Adjust the import according to the actual function name when implemented

def test_scale_empty_recipe():
    # Scaling an empty recipe yields an empty recipe
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_with_factor_one():
    # A factor of one leaves every quantity unchanged
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1, 'flour': 2}

def test_scale_recipe_with_factor_zero():
    # A factor of zero zeroes every quantity
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0, 'flour': 0}

def test_scale_recipe_with_fractional_factor():
    # A factor of 0.5 halves quantities
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.5, 'flour': 1.0}
    # A factor of 1.5 scales quantities to 2.25
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}

def test_scale_recipe_with_large_factor():
    # A factor of 12 multiplies quantities faithfully
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12, 'flour': 24}

def test_rounding_one_third_to_two_decimal_places():
    # One third of one unit comes out as 0.33
    assert scale_recipe({'sugar': 1}, 1/3) == {'sugar': 0.33}

def test_rounding_to_two_decimal_places():
    # 0.1 scaled by three is exactly 0.3
    assert scale_recipe({'sugar': 0.1}, 3) == {'sugar': 0.30}

def test_rounding_to_four_decimal_places():
    # The rounding precision can be chosen explicitly
    assert scale_recipe({'sugar': 1/3}, 1, precision=4) == {'sugar': 0.3333}

def test_negative_scaling_factor():
    # A negative factor is rejected with an error
    with pytest.raises(Exception, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1}, -1)

def test_zero_quantity_ingredient():
    # An ingredient with a zero quantity is rejected
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': 0}, 1)

def test_negative_quantity_ingredient():
    # An ingredient with a negative quantity is rejected
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': -1}, 1)

def test_invalid_ingredient_name():
    # The quantity-validation error names the offending ingredient in quotes
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': -1, 'flour': 2}, 1)

def test_preserving_original_recipe():
    # Scaling returns a new collection; the input recipe is left unmodified
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    assert original == {'sugar': 1, 'flour': 2}
    assert scaled == {'sugar': 2, 'flour': 4}
    assert scaled is not original  # Ensure a new collection is returned

def test_scaled_recipe_contains_original_ingredient_names():
    # The scaled recipe contains exactly the original ingredient names
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    assert set(scaled.keys()) == set(original.keys())
import pytest
from solution import scale_recipe

def test_scale_empty_recipe():
    # Scaling an empty recipe yields an empty recipe
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_with_factor_one():
    # A factor of one leaves every quantity unchanged
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1.00, 'flour': 2.00}

def test_scale_recipe_with_factor_zero():
    # A factor of zero zeroes every quantity
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0.00, 'flour': 0.00}

def test_scale_recipe_with_fractional_factor():
    # A factor of 0.5 halves quantities
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.50, 'flour': 1.00}
    # A factor of 1.5 gives 2.25 for sugar
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}

def test_scale_recipe_with_large_factor():
    # A factor of 12 scales quantities correctly
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12.00, 'flour': 24.00}

def test_scale_recipe_rounding_default():
    # Results are rounded to two decimal places by default
    assert scale_recipe({'ingredient': 1/3}, 1) == {'ingredient': 0.33}
    assert scale_recipe({'ingredient': 0.1}, 3) == {'ingredient': 0.30}

def test_scale_recipe_rounding_custom_precision():
    # The rounding precision can be chosen explicitly
    assert scale_recipe({'ingredient': 1/3}, 1, precision=4) == {'ingredient': 0.3333}

def test_scale_recipe_negative_factor():
    # A negative factor is rejected
    with pytest.raises(ValueError, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1}, -1)

def test_scale_recipe_zero_quantity():
    # An ingredient with a zero quantity is rejected
    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale_recipe({'sugar': 0}, 1)

def test_scale_recipe_negative_quantity():
    # An ingredient with a negative quantity is rejected
    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale_recipe({'sugar': -1}, 1)

def test_scale_recipe_invalid_quantity_name():
    # The quantity-validation error names the offending ingredient
    with pytest.raises(ValueError, match="'sugar' must have a positive quantity"):
        scale_recipe({'sugar': -1}, 1)

def test_preserving_original_recipe():
    original_recipe = {'sugar': 1, 'flour': 2}
    scaled_recipe = scale_recipe(original_recipe, 2)
    # The original recipe is preserved
    assert original_recipe == {'sugar': 1, 'flour': 2}
    # The scaled recipe contains the same ingredient names
    assert scaled_recipe.keys() == original_recipe.keys()
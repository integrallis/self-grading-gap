import pytest
from solution import scale_recipe

def test_scale_empty_recipe():
    # Scaling an empty recipe yields an empty recipe.
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_with_factor_one():
    # A factor of one leaves every quantity unchanged.
    assert scale_recipe({'sugar': 1.0, 'flour': 2.0}, 1) == {'sugar': 1.0, 'flour': 2.0}

def test_scale_recipe_with_factor_zero():
    # A factor of zero zeroes every quantity.
    assert scale_recipe({'sugar': 1.0, 'flour': 2.0}, 0) == {'sugar': 0.0, 'flour': 0.0}

def test_scale_recipe_with_fractional_factor():
    # A factor of 0.5 halves quantities.
    assert scale_recipe({'sugar': 1.0, 'flour': 2.0}, 0.5) == {'sugar': 0.5, 'flour': 1.0}
    # A factor of 1.5 gives 2.25 for sugar.
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}

def test_scale_recipe_with_large_factor():
    # A factor of 12 multiplies faithfully.
    assert scale_recipe({'sugar': 1.0, 'flour': 2.0}, 12) == {'sugar': 12.0, 'flour': 24.0}

def test_rounding_to_two_decimal_places():
    # A third of one unit comes out as 0.33.
    assert scale_recipe({'sugar': 1.0}, 1/3) == {'sugar': 0.33}
    # 0.1 scaled by three is exactly 0.30.
    assert scale_recipe({'sugar': 0.1}, 3) == {'sugar': 0.30}

def test_rounding_with_custom_precision():
    # At four decimal places, a third of one unit comes out as 0.3333.
    assert scale_recipe({'sugar': 1.0}, 1/3) == {'sugar': 0.3333}

def test_negative_scaling_factor():
    # A negative factor is rejected with an error.
    with pytest.raises(Exception, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1.0}, -1)

def test_zero_or_negative_quantity():
    # A zero quantity ingredient is rejected with an error.
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': 0}, 2)
    # A negative quantity ingredient is rejected with an error.
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': -1}, 2)

def test_preserving_original_recipe():
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    scaled_recipe = scale_recipe(original_recipe, 2)
    # Original recipe should be unmodified.
    assert original_recipe == {'sugar': 1.0, 'flour': 2.0}
    # Scaled recipe contains exactly the original ingredient names.
    assert set(scaled_recipe.keys()) == set(original_recipe.keys())
    # Verify that the scaled recipe is a new collection.
    assert scaled_recipe is not original_recipe